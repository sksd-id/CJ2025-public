use std::collections::HashSet;

use blake2::{digest, Digest};

use ark_bn254::{Bn254, Fr};
use ark_ff::{Fp256, PrimeField, UniformRand};
use ark_groth16::{Groth16, Proof, ProvingKey, VerifyingKey};
use ark_r1cs_std::alloc::AllocVar;
use ark_r1cs_std::{eq::EqGadget, fields::fp::FpVar, R1CSVar};
use ark_relations::r1cs::{ConstraintSynthesizer, ConstraintSystemRef, SynthesisError};
use ark_serialize::{CanonicalDeserialize, CanonicalSerialize};
use ark_snark::SNARK;
use arkworks_native_gadgets::poseidon::{
    sbox::PoseidonSbox, FieldHasher, Poseidon, PoseidonParameters,
};
use arkworks_r1cs_gadgets::poseidon::{FieldHasherGadget, PoseidonGadget};
use arkworks_utils::{
    bytes_matrix_to_f, bytes_vec_to_f, poseidon_params::setup_poseidon_params, Curve,
};
use serde::Deserialize;
use serde::Serialize;

fn poseidon() -> Poseidon<Fr> {
    let data = setup_poseidon_params(Curve::Bn254, 5, 3).unwrap();

    let params = PoseidonParameters {
        mds_matrix: bytes_matrix_to_f(&data.mds),
        round_keys: bytes_vec_to_f(&data.rounds),
        full_rounds: data.full_rounds,
        partial_rounds: data.partial_rounds,
        sbox: PoseidonSbox(data.exp),
        width: data.width,
    };

    Poseidon::<Fr>::new(params)
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Ticket {
    pub proof: String,
    pub vk_bytes: Option<[u8; 32]>,
    pub flip_index: Option<usize>,
}

#[derive(Copy, Clone)]
pub struct TicketVirtuosoCircuit<F: PrimeField> {
    pub secret: Option<F>,
}

impl ConstraintSynthesizer<Fr> for TicketVirtuosoCircuit<Fr> {
    fn generate_constraints(self, cs: ConstraintSystemRef<Fr>) -> Result<(), SynthesisError> {
        // create the poseidon gadget
        let poseidon = PoseidonGadget::from_native(&mut cs.clone(), poseidon())?;

        // witness the secret
        let secret = FpVar::new_witness(cs.clone(), || Ok(self.secret.unwrap()))?;
        let hash = poseidon.hash(&[secret])?;

        // input the hash and enforce equality
        FpVar::new_input(cs.clone(), || hash.value())?.enforce_equal(&hash)?;
        Ok(())
    }
}

const INF_BYTES: [u8; 32] = {
    let mut arr = [0u8; 32];
    arr[31] = 64;
    arr
};

const FORBIDDEN_DIGESTS: [&str; 11] = [
    "0000000000000000000000000000000000000000000000000000000000000000",
    "000000f093f5e1439170b97948e833285d588181b64550b829a031e1724e6430",
    "010000e027ebc38722e172f390d06750bab002036d8ba070534063c2e59cc860",
    "020000d0bbe0a5cbb3512c6dd9b89b781709848423d1f0287de094a358eb2c91",
    "030000c04fd6870f45c2e5e621a1cfa074610506da1641e1a680c684cb3991c1",
    "040000b0e3cb6953d6329f606a8903c9d1b98687905c9199d020f8653e88f5f1",
    "010000f093f5e1439170b97948e833285d588181b64550b829a031e1724e6430",
    "020000e027ebc38722e172f390d06750bab002036d8ba070534063c2e59cc860",
    "030000d0bbe0a5cbb3512c6dd9b89b781709848423d1f0287de094a358eb2c91",
    "040000c04fd6870f45c2e5e621a1cfa074610506da1641e1a680c684cb3991c1",
    "050000b0e3cb6953d6329f606a8903c9d1b98687905c9199d020f8653e88f5f1",
];

pub struct TicketVirtuoso {
    secret: Fr,
    digest: Fr,
    spent: HashSet<[u8; 32]>, // spent ticket ids
    pk: ProvingKey<Bn254>,    // proving key
    vk: VerifyingKey<Bn254>,  // verifying key
}

impl TicketVirtuoso {
    pub fn digest(&self) -> String {
        let mut bs = vec![];
        self.digest.serialize(&mut bs).unwrap();
        hex::encode(bs[..30].to_vec())
    }

    pub fn ticket_verify(&self, ticket: Ticket) -> Result<[u8; 32], anyhow::Error> {
        // deserialize the ticket
        let proof = hex::decode(ticket.proof)?;
        let proof = Proof::<Bn254>::deserialize(&proof[..])?;

        // additional protection
        if proof.a.infinity || proof.b.infinity || proof.c.infinity {
            return Err(anyhow::Error::msg("Invalid ticket"));
        }

        let mut vk_bytes = vec![];
        let mut verifying_key = self.vk.clone();
        verifying_key.serialize(&mut vk_bytes)?;

        if ticket.vk_bytes.is_some() && ticket.flip_index.is_some() {
            if ticket.vk_bytes.unwrap() == INF_BYTES {
                return Err(anyhow::Error::msg("Invalid ticket"));
            }

            let insert_pos = ticket.flip_index.unwrap();
            vk_bytes.splice(
                insert_pos..insert_pos + 32,
                ticket.vk_bytes.unwrap().iter().cloned(),
            );

            verifying_key = VerifyingKey::<Bn254>::deserialize(&vk_bytes[..])?;
        }

        if !Groth16::<Bn254>::verify(&verifying_key, &[self.digest], &proof)? {
            return Err(anyhow::Error::msg("Invalid ticket"));
        }

        // compute the ticket id
        let mut ser = vec![];
        self.digest.serialize(&mut ser).unwrap();
        proof.serialize(&mut ser).unwrap();
        Ok(blake2::Blake2b::digest(&ser).into())
    }

    pub fn issue(&self) -> Result<Ticket, SynthesisError> {
        // create fresh ticket
        let circuit = TicketVirtuosoCircuit {
            secret: Some(self.secret),
        };
        let proof = Groth16::<Bn254>::prove(&self.pk, circuit, &mut rand::thread_rng())?;

        // serialize the proof
        let mut bs = vec![];
        proof.serialize(&mut bs).unwrap();
        Ok(Ticket {
            proof: hex::encode(bs),
            vk_bytes: None,
            flip_index: None,
        })
    }

    pub fn redeem(&mut self, ticket: Ticket) -> bool {
        match self.ticket_verify(ticket) {
            Ok(id) => self.spent.insert(id),
            Err(_) => false,
        }
    }

    pub fn setup() -> Self {
        let mut rng = rand::thread_rng();
        let circuit = TicketVirtuosoCircuit { secret: None };
        let (pk, vk) =
            Groth16::<Bn254>::circuit_specific_setup(circuit, &mut rand::thread_rng()).unwrap();
        let secret = Fr::rand(&mut rng);
        let digest = poseidon().hash(&[secret]).unwrap();

        Self {
            pk,
            vk,
            secret,
            digest,
            spent: HashSet::new(),
        }
    }

    pub fn pk(&self) -> String {
        let mut bs = vec![];
        self.pk.serialize(&mut bs).unwrap();
        hex::encode(bs)
    }

    pub fn vk(&self) -> String {
        let mut bs = vec![];
        self.vk.serialize(&mut bs).unwrap();
        hex::encode(bs)
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Request {
    Redeem(Ticket),
    Balance,
    BuyFlag,
    BuyTicket,
    ProvingKey,
    VerifyingKey,
    Digest,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Response {
    Hello(String),
    Ticket(Ticket),
    ProvingKey(String),
    VerifyingKey(String),
    GoodTicket,
    BadTicket,
    LolTooPoor,
    NotAllowed,
    Balance(i64),
    Flag(String),
    Digest(String),
}

#[test]
fn test() {
    let mut virtuoso = TicketVirtuoso::setup();
    let ticket = virtuoso.issue().unwrap();
    assert!(virtuoso.redeem(ticket.clone()));
    assert!(!virtuoso.redeem(ticket.clone()));
}
