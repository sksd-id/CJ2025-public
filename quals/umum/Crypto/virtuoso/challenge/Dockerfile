FROM ubuntu:22.04

# install rust and socat
RUN apt-get update && apt-get install -y curl socat build-essential 
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Cargo.toml and Cargo.lock are copied first to cache dependencies
COPY Cargo.toml Cargo.lock /app/

RUN mkdir /app/src

# copy the source code
COPY src/virtuoso.rs /app/src/virtuoso.rs
COPY src/main.rs /app/src/main.rs

WORKDIR /app

# build the source code
RUN cargo build --release

# copy the flag into the image
COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt

# run the server
RUN printf '%s\n' \
  '#!/bin/sh' \
  'set -eu' \
  'export FLAG="$(tr -d '\''\r\n'\'' < /flag.txt)"' \
  'exec socat TCP-LISTEN:8001,reuseaddr,fork EXEC:"/app/target/release/virtuoso"' \
  > /entrypoint.sh \
  && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
