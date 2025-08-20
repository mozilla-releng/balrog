# WARNING: keep this file in sync with agent/Dockerfile

FROM python:3.13-slim-bookworm

MAINTAINER jcristau@mozilla.com

ENV LC_ALL C.UTF-8

WORKDIR /app

# %include agent/requirements
COPY topsrcdir/agent/requirements/ /app/requirements/
RUN pip install -r requirements/base.txt

# %include agent/src
COPY topsrcdir/agent/src/ /app/src/
# %include agent/tests
COPY topsrcdir/agent/tests/ /app/tests/
# %include agent/scripts
COPY topsrcdir/agent/scripts/ /app/scripts/
# %include agent/run.sh
# %include agent/MANIFEST.in
# %include agent/pyproject.toml
# %include agent/setup.py
# %include agent/version.json
COPY topsrcdir/agent/run.sh topsrcdir/agent/MANIFEST.in topsrcdir/agent/pyproject.toml topsrcdir/agent/setup.py topsrcdir/agent/version.json /app/
# test-only stuff
# %include agent/tox.ini
# %include agent/version.txt
COPY topsrcdir/agent/tox.ini topsrcdir/agent/version.txt /app/

RUN pip install .

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["agent"]
