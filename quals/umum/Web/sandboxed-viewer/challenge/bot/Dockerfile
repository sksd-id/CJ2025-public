FROM node:20-alpine

# Install system Chromium for Puppeteer (headless)
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --omit=dev

COPY server.js ./

EXPOSE 3001

ENV NODE_ENV=production \
    PUPPETEER_SKIP_DOWNLOAD=true \
    CHROMIUM_PATH=/usr/bin/chromium
CMD ["node", "server.js"]
