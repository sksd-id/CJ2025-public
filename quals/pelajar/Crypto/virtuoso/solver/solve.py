import json
from pwn import remote

# pip install zksnake
from zksnake.ecc import EllipticCurve
from zksnake.groth16 import Proof, VerifyingKey
from zksnake.utils import get_random_int


def getVerifyingKey(io):
    io.sendline(b'"VerifyingKey"')
    resp = io.readline().decode()
    return resp


def redeemTicket(rem, ticket_proof):
    payload = {"Redeem": ticket_proof}
    print(json.dumps(payload))
    rem.sendline(json.dumps(payload).encode())

    resp = rem.readline().decode()
    return resp


def rerandomize_proof(proof):
    global E

    r = get_random_int(E.order)
    s = get_random_int(E.order)

    new_A = pow(r, -1, E.order) * proof.A
    new_B = r * proof.B + r * s * vk.delta_2
    new_C = proof.C + s * proof.A

    return Proof(new_A, new_B, new_C).to_bytes().hex()


E = EllipticCurve("BN254")

io = remote("0.0.0.0", 8001)
io.readline()

vk = VerifyingKey.from_bytes(
    bytes.fromhex(json.loads(getVerifyingKey(io))["VerifyingKey"])[:296]
)
infinity_point = E.G1() * 0
negative_one = (E.order - 1).to_bytes(32, "little")
ic_0 = vk.ic[0]

proof = Proof(vk.alpha_1, vk.beta_2, infinity_point)

for _ in range(20):
    ticket_proof = rerandomize_proof(proof)
    ticket = {
        "proof": ticket_proof,
        "digest": negative_one.hex(),
        "vk_bytes": list(ic_0.to_bytes()),
        "flip_index": 224 + 8 + 32,
    }
    redeemed = redeemTicket(io, ticket)
    print(f"redeemed ticket = {redeemed}")

io.sendline(b'"BuyFlag"')
io.interactive()
