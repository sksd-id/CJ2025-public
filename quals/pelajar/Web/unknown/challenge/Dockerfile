FROM oven/bun:slim

RUN apt update && apt install -y gcc

RUN useradd ctf

COPY ./app/package.json /app/package.json

WORKDIR /app

RUN bun i

COPY ./app/ /app

COPY ./flag.txt /root/flag.txt
RUN chmod 400 /root/flag.txt

COPY ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod +s /readflag
RUN rm /readflag.c

USER ctf
ENV NODE_ENV=production
CMD ["bun", "src/index.ts"]

