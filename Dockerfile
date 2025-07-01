# WARNING: keep this file in sync with taskcluster/docker/balrog-backend/Dockerfile

FROM python:3.13-slim

ENV LC_ALL C.UTF-8

LABEL maintainer="releng@mozilla.com"

# default-libmysqlclient-dev is required to use SQLAlchemy with MySQL, which we do in production.
# xz-utils is needed to compress production database dumps
RUN apt-get -q update \
    && apt-get -q --yes install default-libmysqlclient-dev mariadb-client xz-utils pkg-config \
    && apt-get clean

WORKDIR /app

# install the requirements into the container first
# these rarely change and is more cache friendly
# ... really speeds up building new containers
COPY requirements/ /app/requirements/
RUN apt-get install -q --yes gcc && \
    pip install --no-deps -r requirements/base.txt && \
    apt-get -q --yes remove gcc && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.cache

# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
COPY src/ /app/src/
COPY uvicorn/ /app/uvicorn/
COPY scripts/manage-db.py scripts/run-batch-deletes.sh scripts/run.sh scripts/reset-stage-db.sh scripts/get-prod-db-dump.py /app/scripts/
COPY MANIFEST.in pyproject.toml setup.py version.json version.txt /app/

RUN pip install .

WORKDIR /app

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
CMD ["public"]
