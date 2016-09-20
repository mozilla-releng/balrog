FROM python:2.7-slim

MAINTAINER bhearsum@mozilla.com

# Some versions of the python:2.7 Docker image remove libpcre3, which
# uwsgi needs for routing support to be enabled.
# We may be able to remove this after https://github.com/docker-library/python/pull/137
# is fixed.
# Node and npm are to build the frontend. nodejs-legacy is needed by this version of npm.
# libmysqlclient-dev is required to use SQLAlchemy with MySQL, which we do in production.
# libfontconfig1 is required by phantomjs
RUN apt-get -q update \
    && apt-get -q --yes install libpcre3 libpcre3-dev nodejs nodejs-legacy npm libmysqlclient-dev \
                                libfontconfig1 \
    && apt-get clean

WORKDIR /app

# install the requirements into the container first
# these rarely change and is more cache friendly
# ... really speeds up building new containers
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy in sources after
# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
COPY auslib/ /app/auslib/
COPY ui/ /app/ui/
COPY uwsgi/ /app/uwsgi/
COPY scripts/ /app/scripts/
COPY MANIFEST.in setup.py version.json /app/
# These files are only needed for CI, but they're not very big so we may as
# well just include them here to avoid forking the Dockerfile.
COPY .coveragerc requirements-test.txt run-tests.sh tox.ini version.txt /app/
COPY aus-data-snapshots/ /app/aus-data-snapshots/

WORKDIR /app/ui
RUN npm install
RUN npm run build

WORKDIR /app

ENTRYPOINT ["/app/uwsgi/run.sh"]
CMD ["public"]
