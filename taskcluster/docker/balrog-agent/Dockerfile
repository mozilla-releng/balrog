FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim@sha256:d8a45a30929a5bfedd8b09d630538ca1ab30041154d2a6cb2e4fee3cffd3ea4c AS builder

WORKDIR /app

# Use an arg so we can share the Dockerfile with docker compose
ARG SRC=topsrcdir

# %include pyproject.toml
# %include uv.lock
# %include README.rst
COPY ${SRC}/pyproject.toml ${SRC}/uv.lock ${SRC}/README.rst /app/

# %include agent
COPY ${SRC}/agent /app/agent

RUN uv venv
RUN uv sync --package=balrogagent --frozen --no-dev

FROM python:3.13-slim-trixie@sha256:eb43ff125d8d58d7449dcba7d336c23bcac412f526d861db493b9994d8010280
WORKDIR /app
ENV LC_ALL C.UTF-8
LABEL maintainer="releng@mozilla.com"

COPY --from=builder /app/.venv /app/.venv

# %include agent/scripts
# %include agent/src
# %include agent/run.sh
COPY ${SRC}/agent/scripts/ /app/scripts/
COPY ${SRC}/agent/src /app/agent/src
COPY ${SRC}/agent/run.sh /app

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["agent"]
