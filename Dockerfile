FROM python:3.7-slim-stretch

MAINTAINER bhearsum@mozilla.com

# Some versions of the python:3.7 Docker image remove libpcre3, which uwsgi needs for routing support to be enabled.
# Node and npm are to build the frontend. nodejs-legacy is needed by this version of npm. These will get removed after building.
# default-libmysqlclient-dev is required to use SQLAlchemy with MySQL, which we do in production.
# xz-utils is needed to compress production database dumps
RUN apt-get -q update \
    && apt-get -q --yes install libpcre3 libpcre3-dev default-libmysqlclient-dev mysql-client xz-utils \
    && apt-get clean

WORKDIR /app

# install the requirements into the container first
# these rarely change and is more cache friendly
# ... really speeds up building new containers
COPY requirements/ /app/requirements/
RUN apt-get install -q --yes gcc && \
    pip install -r requirements/base.txt && \
    apt-get -q --yes remove gcc && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.cache

# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
COPY auslib/ /app/auslib/
COPY ui/ /app/ui/
COPY uwsgi/ /app/uwsgi/
COPY scripts/manage-db.py scripts/run-batch-deletes.sh scripts/run.sh scripts/reset-stage-db.sh scripts/get-prod-db-dump.py scripts/releases-history-to-gcs.py /app/scripts/
COPY version.json /app/

WORKDIR /app

RUN cd ui && \
    echo "deb http://deb.debian.org/debian stretch-backports main" > /etc/apt/sources.list.d/stretch-backports.list && \
    apt-get -q update && \
    apt-get -q --yes install -t stretch-backports git nodejs npm && \
    npm install && \
    npm run build && \
    rm /etc/apt/sources.list.d/stretch-backports.list && \
    apt-get -q --yes remove nodejs npm && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.npm /tmp/phantomjs && \
    find . -maxdepth 1 -not -name dist -exec rm -rf {} \;

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
CMD ["public"]
