FROM python:3.6-slim

MAINTAINER bhearsum@mozilla.com

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY balrogagent/ /app/balrogagent/
COPY scripts/ /app/scripts/
COPY run.sh MANIFEST.in setup.py version.json /app/
# test-only stuff
COPY .coveragerc requirements-tox.txt requirements-test.txt run-tests.sh tox.ini version.txt /app/

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["agent"]
