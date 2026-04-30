FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim@sha256:3a99382378e1d3d67c6d671cddbfd7a17f3b064db802c3afe9d29406c36a6dc2 AS builder

WORKDIR /app

# default-libmysqlclient-dev is required to use SQLAlchemy with MySQL
# gcc is needed to compile some python packages
# uwsgi needs libpcre for routing support to be enabled
RUN apt-get -q update \
    && apt-get -q --yes install g++ default-libmysqlclient-dev gcc pkg-config libpcre2-dev

# Use a variable so we can share the Dockerfile with docker compose
ARG SRC=topsrcdir

# %include pyproject.toml
# %include uv.lock
# %include README.rst
COPY ${SRC}/pyproject.toml ${SRC}/uv.lock ${SRC}/README.rst /app/
# %include src
COPY ${SRC}/src/ /app/src/

RUN uv venv
RUN uv sync --no-dev --frozen

FROM python:3.13-slim-trixie@sha256:a0779d7c12fc20be6ec6b4ddc901a4fd7657b8a6bc9def9d3fde89ed5efe0a3d
ENV LC_ALL C.UTF-8
LABEL maintainer="releng@mozilla.com"

# netcat is needed for health checks
# libpcre is needed by uwsgi (see above)
# mariadb-client is needed to import sample data
# curl is needed to pull sample data
# xz-utils is needed to unpack sample data
RUN apt-get -q update \
    && apt-get -q --yes install netcat-traditional libpcre2-8-0 mariadb-client curl xz-utils \
    && apt-get clean

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
# %include src
COPY ${SRC}/src/ /app/src/
# %include scripts
COPY ${SRC}/scripts/ /app/scripts/
# %include uwsgi
COPY ${SRC}/uwsgi/ /app/uwsgi/
# %include version.json
COPY ${SRC}/version.json /app/

ENV PATH="/app/.venv/bin:${PATH}"

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
CMD ["public"]
