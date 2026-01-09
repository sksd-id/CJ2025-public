#!/bin/bash
set -e

node /app/server.js &
NODE_PID=$!

trap "kill -TERM ${NODE_PID}; wait ${NODE_PID}" SIGINT SIGTERM

exec apachectl -DFOREGROUND
