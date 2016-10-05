#!/bin/bash

# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
docker build  -t balrogtest -f Dockerfile.dev .
# Using a volume mount here ensures that the tox cache dir ends up on the host,
# which avoids re-installing test dependencies every single time.
docker run --rm balrogtest test $@
