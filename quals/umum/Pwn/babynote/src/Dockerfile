FROM ubuntu:24.04

RUN apt update -y
RUN apt install python3 socat adduser -y

RUN adduser --disabled-password --uid 1001 --shell /bin/bash ctf

COPY ./babynote /home/ctf/
COPY ./run.sh /home/ctf/
COPY ./flag /home/ctf/

WORKDIR /home/ctf/
RUN mv ./flag ./flag-$(md5sum flag | awk '{print $1}')

RUN chown -R root:root /home/ctf/
RUN chmod -R 555 /home/ctf/
USER ctf


CMD ["./run.sh"]