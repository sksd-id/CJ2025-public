FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m corestock
WORKDIR /home/corestock

COPY main.py /home/corestock/

RUN chown -R root:root /home/corestock && \
    chmod -R 555 /home/corestock

EXPOSE 5111

ENTRYPOINT ["socat", "TCP-LISTEN:5111,reuseaddr,fork,nodelay,su=corestock", "EXEC:'timeout 60 python3 main.py'"]