FROM node:20-alpine AS builder

WORKDIR /app

COPY ./build/package.json .

RUN npm install

COPY ./build .

RUN npm run build

FROM nginx:latest

COPY --from=builder /app/dist /var/www/html

EXPOSE 80