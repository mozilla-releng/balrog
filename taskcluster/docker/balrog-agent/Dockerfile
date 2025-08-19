# WARNING: keep this file in sync with agent/Dockerfile

ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder

WORKDIR /app

# %include pyproject.toml
# %include uv.lock
# %include README.rst
COPY topsrcdir/pyproject.toml topsrcdir/uv.lock topsrcdir/README.rst /app/

# %include agent
COPY topsrcdir/agent /app/agent

RUN uv venv
RUN uv sync --package=balrogagent --frozen --no-dev

FROM python:${PYTHON_VERSION}-slim-bookworm
WORKDIR /app
ENV LC_ALL C.UTF-8
LABEL maintainer="releng@mozilla.com"

COPY --from=builder /app/.venv /app/.venv

# %include agent/scripts
# %include agent/src
# %include agent/run.sh
COPY topsrcdir/agent/scripts/ /app/scripts/
COPY topsrcdir/agent/src /app/agent/src
COPY topsrcdir/agent/run.sh /app

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["agent"]
