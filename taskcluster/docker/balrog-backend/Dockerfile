# WARNING: keep this file in sync with the main balrog Dockerfile

FROM python:3.13-slim

ENV LC_ALL C.UTF-8

# uwsgi needs libpcre3 for routing support to be enabled.
# default-libmysqlclient-dev is required to use SQLAlchemy with MySQL, which we do in production.
# xz-utils is needed to compress production database dumps
RUN apt-get -q update \
    && apt-get -q --yes install libpcre3-dev default-libmysqlclient-dev mariadb-client xz-utils pkg-config \
    && apt-get clean

WORKDIR /app

# install the requirements into the container first
# these rarely change and is more cache friendly
# ... really speeds up building new containers
# %include requirements
COPY topsrcdir/requirements/ /app/requirements/
RUN apt-get install -q --yes gcc && \
    pip install --no-deps -r requirements/base.txt && \
    apt-get -q --yes remove gcc && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.cache

# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
# %include src
COPY topsrcdir/src/ /app/src/
# %include uwsgi
COPY topsrcdir/uwsgi/ /app/uwsgi/
# %include scripts
COPY topsrcdir/scripts/manage-db.py topsrcdir/scripts/run-batch-deletes.sh topsrcdir/scripts/run.sh topsrcdir/scripts/reset-stage-db.sh topsrcdir/scripts/get-prod-db-dump.py /app/scripts/
# %include MANIFEST.in
# %include pyproject.toml
# %include setup.py
# %include version.json
# %include version.txt
COPY topsrcdir/MANIFEST.in topsrcdir/pyproject.toml topsrcdir/setup.py topsrcdir/version.json topsrcdir/version.txt /app/

RUN pip install .

WORKDIR /app

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
CMD ["public"]
