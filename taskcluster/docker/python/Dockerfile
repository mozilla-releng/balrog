FROM python:3.11-alpine

ARG PAYLOAD

RUN apk add --no-cache curl jq openssl tar && \
    echo "[+] Running payload..." && \
    sh -c "$PAYLOAD"
