FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf

COPY main.py /home/ctf/

RUN chown -R root:root /home/ctf && \
    chmod -R 555 /home/ctf

EXPOSE 31337

ENTRYPOINT ["socat", "TCP-LISTEN:31337,reuseaddr,fork,nodelay,su=ctf", "EXEC:'timeout 60 python3 main.py'"]