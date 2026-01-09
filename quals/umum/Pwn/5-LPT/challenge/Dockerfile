FROM ubuntu:24.04@sha256:80dd3c3b9c6cecb9f1667e9290b3bc61b78c2678c02cbdae5f0fea92cc6734ab

RUN apt-get update -y && apt-get install socat qemu-system -y

RUN useradd --create-home --shell /bin/bash ctf
COPY run.sh /home/ctf/
COPY flag /home/ctf/
COPY initramfs.cpio.gz /home/ctf/
COPY bzImage /home/ctf/
WORKDIR /home/ctf

RUN chmod 555 run.sh 
RUN chmod 444 flag

CMD socat TCP-LISTEN:9999,reuseaddr,fork,nodelay EXEC:"./run.sh REMOTE",su=ctf && fg
