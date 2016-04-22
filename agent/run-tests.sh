#!/bin/bash

# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
docker build --pull -t balrogagenttest .
docker run --entrypoint /app/scripts/test-entrypoint.sh balrogagenttest
