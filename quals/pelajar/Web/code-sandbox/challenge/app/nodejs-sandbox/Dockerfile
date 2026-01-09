FROM node:20-slim

RUN apt-get update && apt-get install -y gcc curl netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

COPY ./flag.txt /root/flag.txt
RUN chmod 400 /root/flag.txt

COPY ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod +s /readflag
RUN rm /readflag.c

WORKDIR /app

COPY app/nodejs-sandbox/package.json .
RUN npm install --production

COPY app/nodejs-sandbox/src/ ./src/

RUN chown -R ctf:ctf /app

USER ctf

ENV NODE_ENV=production

EXPOSE 3000

CMD ["sh", "-c", "timeout 60 node src/index.js; exit 0"]
