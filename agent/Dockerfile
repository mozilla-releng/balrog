FROM python:3.5-slim

MAINTAINER bhearsum@mozilla.com

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY balrogagent/ /app/balrogagent/
COPY scripts/ /app/scripts/
COPY MANIFEST.in setup.py version.json /app/
# test-only stuff
COPY .coveragerc requirements-test.txt run-tests.sh tox.ini version.txt /app/

ENTRYPOINT ["/usr/local/bin/python"]
CMD ["-m", "balrogagent.cmd"]
