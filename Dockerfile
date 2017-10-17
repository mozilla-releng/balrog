FROM python:2.7-slim

MAINTAINER bhearsum@mozilla.com

# Some versions of the python:2.7 Docker image remove libpcre3, which uwsgi needs for routing support to be enabled.
# Node and npm are to build the frontend. nodejs-legacy is needed by this version of npm. These will get removed after building.
# libmysqlclient-dev is required to use SQLAlchemy with MySQL, which we do in production.
RUN apt-get -q update \
    && apt-get -q --yes install libpcre3 libpcre3-dev libmysqlclient-dev mysql-client \
    && apt-get clean

WORKDIR /app

# install the requirements into the container first
# these rarely change and is more cache friendly
# ... really speeds up building new containers
COPY requirements.txt /app/
RUN apt-get install -q --yes gcc && \
    pip install -r requirements.txt && \
    apt-get -q --yes remove gcc && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.cache

# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
COPY auslib/ /app/auslib/
COPY ui/ /app/ui/
COPY uwsgi/ /app/uwsgi/
COPY scripts/manage-db.py scripts/run-batch-deletes.sh scripts/run.sh scripts/reset-stage-db.sh /app/scripts/
COPY version.json /app/

WORKDIR /app

RUN cd ui && \
    apt-get -q --yes install nodejs nodejs-legacy npm && \
    npm install && \
    npm run build && \
    apt-get -q --yes remove nodejs nodejs-legacy npm && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.npm /tmp/phantomjs && \
    find . -maxdepth 1 -not -name dist -exec rm -rf {} \;

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
CMD ["public"]
