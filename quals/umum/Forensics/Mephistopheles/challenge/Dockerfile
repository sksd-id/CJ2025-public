FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m mephisto
WORKDIR /home/mephisto

COPY main.py /home/mephisto/

RUN chown -R root:root /home/mephisto && \
    chmod -R 555 /home/mephisto

EXPOSE 5113

ENTRYPOINT ["socat", "TCP-LISTEN:5113,reuseaddr,fork,nodelay,su=mephisto", "EXEC:'timeout 60 python3 main.py'"]