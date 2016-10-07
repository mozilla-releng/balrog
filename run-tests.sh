#!/bin/bash

# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
docker build  -t balrogtest -f Dockerfile.dev .
# We can't use a volume mount here because this script is used for local
# tests as well as CI, and Taskcluster doesn't support volume mounts.
docker run --rm balrogtest test $@
