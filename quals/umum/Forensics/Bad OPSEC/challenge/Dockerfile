FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m badopsecc
WORKDIR /home/badopsecc

COPY main.py /home/badopsecc/

RUN chown -R root:root /home/badopsecc && \
    chmod -R 555 /home/badopsecc

EXPOSE 5112

ENTRYPOINT ["socat", "TCP-LISTEN:5112,reuseaddr,fork,nodelay,su=badopsecc", "EXEC:'timeout 60 python3 main.py'"]