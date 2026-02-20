FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim@sha256:531f855bda2c73cd6ef67d56b733b357cea384185b3022bd09f05e002cd144ca AS builder

WORKDIR /app

# default-libmysqlclient-dev is required to use SQLAlchemy with MySQL
# gcc is needed to compile some python packages
RUN apt-get -q update \
    && apt-get -q --yes install g++ default-libmysqlclient-dev gcc pkg-config

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

FROM python:3.13-slim-bookworm@sha256:8092ae2ef67061f9db412458dbdce44dbf16748fb3cae5cdbd020f467a9712d0
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
