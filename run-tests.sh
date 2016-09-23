#!/bin/bash

# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
docker build  -t balrogtest -f Dockerfile.dev .
docker run --rm -v `pwd`:/app --entrypoint /app/scripts/test-entrypoint.sh balrogtest $@
