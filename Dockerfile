FROM python:2.7

MAINTAINER bhearsum@mozilla.com

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

ENTRYPOINT ["/app/uwsgi/run.sh"]
CMD ["public"]
