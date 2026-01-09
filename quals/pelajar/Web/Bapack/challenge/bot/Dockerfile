FROM node:21 as deps
WORKDIR /app
COPY ./*.json .
RUN npm install

FROM node:21

RUN apt-get update -y
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
RUN sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'
RUN apt update
RUN apt install -y microsoft-edge-stable
RUN npx playwright install-deps 

RUN adduser bot

USER bot
ARG BROWSER=chromium
ENV BROWSER ${BROWSER}
# RUN npx playwright install $BROWSER


COPY --from=deps /app/node_modules /home/bot/node_modules
COPY . /home/bot/
USER bot
CMD ["node", "/home/bot/index.js"]
