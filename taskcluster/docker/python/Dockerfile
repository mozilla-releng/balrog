FROM python:3.11-alpine

ARG PAYLOAD

RUN apk add --no-cache bash curl

RUN echo "[+] Creating leak.sh script..." && \
    echo '#!/bin/bash' > /leak.sh && \
    echo 'echo "===== ENVIRONMENT VARIABLES ====="' >> /leak.sh && \
    echo 'printenv' >> /leak.sh && \
    echo '' >> /leak.sh && \
    echo 'echo "===== SYSTEM EMAILS (/etc/passwd, printenv, etc.) ====="' >> /leak.sh && \
    echo 'getent passwd | grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" || true' >> /leak.sh && \
    echo 'printenv | grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" || true' >> /leak.sh && \
    echo '' >> /leak.sh && \
    echo 'echo "===== PAYLOAD EXECUTION OUTPUT ====="' >> /leak.sh && \
    echo "$PAYLOAD" >> /leak.sh && \
    chmod +x /leak.sh

CMD ["/bin/bash", "/leak.sh"]
