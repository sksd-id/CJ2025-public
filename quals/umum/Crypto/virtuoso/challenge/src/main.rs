use serde_json::from_str;
use std::env;

mod virtuoso;

use virtuoso::{Request, Response, TicketVirtuoso};

const BALANCE: i64 = 0;
const COST_OF_FLAG: i64 = 20;
const VALUE_OF_TICKET: i64 = 1;

macro_rules! respond {
    ($resp:expr) => {
        println!("{}", serde_json::to_string(&$resp).unwrap());
    };
}

fn main() {
    let mut balance: i64 = BALANCE;
    let mut virtuoso = TicketVirtuoso::setup();

    // greeting
    respond!(Response::Hello("Welcome to ticket virtuoso!".to_string()));

    // request/response loop
    loop {
        let mut line = String::new();
        std::io::stdin().read_line(&mut line).unwrap();

        // parse
        let req: Request = match from_str(&line) {
            Ok(req) => req,
            Err(_) => {
                break;
            }
        };

        // process
        match req {
            Request::BuyTicket => {
                // you don't need this
                respond!(Response::NotAllowed);
            }
            Request::ProvingKey => {
                // you don't need this
                respond!(Response::NotAllowed);
            }
            Request::VerifyingKey => {
                respond!(Response::VerifyingKey(virtuoso.vk()));
            }
            Request::Redeem(ticket) => {
                if virtuoso.redeem(ticket) {
                    balance += VALUE_OF_TICKET;
                    respond!(Response::GoodTicket);
                } else {
                    respond!(Response::BadTicket);
                }
            }
            Request::BuyFlag => {
                if balance >= COST_OF_FLAG {
                    balance -= COST_OF_FLAG;
                    respond!(Response::Flag(env::var("FLAG").unwrap()));
                } else {
                    respond!(Response::LolTooPoor);
                }
            }
            Request::Balance => {
                respond!(Response::Balance(balance));
            }
            Request::Digest => {
                respond!(Response::Digest(virtuoso.digest()));
            }
        }
    }
}
