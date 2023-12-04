# WARNING: keep this file in sync with taskcluster/docker/balrog-agent/Dockerfile

FROM python:3.11-slim

MAINTAINER jcristau@mozilla.com

WORKDIR /app

COPY requirements/ /app/requirements/
RUN pip install -r requirements/base.txt

COPY src/ /app/src/
COPY tests/ /app/tests/
COPY scripts/ /app/scripts/
COPY run.sh MANIFEST.in pyproject.toml setup.py version.json /app/
# test-only stuff
COPY version.txt /app/

RUN python setup.py install

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["agent"]
