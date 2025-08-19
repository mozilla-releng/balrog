# WARNING: keep this file in sync with taskcluster/docker/balrog-backend/Dockerfile
ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder

WORKDIR /app

# default-libmysqlclient-dev is required to use SQLAlchemy with MySQL
# gcc is needed to compile some python packages
RUN apt-get -q update \
    && apt-get -q --yes install g++ default-libmysqlclient-dev gcc pkg-config

COPY pyproject.toml uv.lock README.rst /app
COPY src/ /app/src/
RUN uv venv
RUN uv sync --no-dev --frozen

FROM python:${PYTHON_VERSION}-slim-bookworm
ENV LC_ALL C.UTF-8
LABEL maintainer="releng@mozilla.com"

# netcat is needed for health checks
# Some versions of the python:3.8 Docker image remove libpcre3, which uwsgi needs for routing support to be enabled.
# mariadb-client is needed to import sample data
# curl is needed to pull sample data
# xz-utils is needed to unpack sampled ata
RUN apt-get -q update \
    && apt-get -q --yes install netcat-traditional libpcre3 mariadb-client curl xz-utils \
    && apt-get clean

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY scripts/ /app/scripts/
COPY uwsgi/ /app/uwsgi/
COPY version.json /app/

ENV PATH="/app/.venv/bin:${PATH}"

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
CMD ["public"]
