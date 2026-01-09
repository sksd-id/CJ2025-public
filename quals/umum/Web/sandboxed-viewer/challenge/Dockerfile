FROM ubuntu:24.04

# Install Apache HTTP Server and Node.js with npm and Express
RUN apt-get update \
    && apt-get install -y --no-install-recommends apache2 nodejs npm \
    && a2enmod proxy proxy_http headers \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /files
COPY files/ /files/

# Copy any custom Apache configuration snippets
COPY apache2/ /etc/apache2/conf-enabled/

# Copy Express app and start script
WORKDIR /app
COPY app/package*.json /app/
RUN npm ci --omit=dev
COPY app/ /app/
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

EXPOSE 80

# Start Express then Apache in the foreground so the container stays alive
CMD ["/usr/local/bin/start.sh"]
