#!/bin/bash

# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
docker build --pull -t balrogagenttest .
# We can't use a volume mount in Taskcluster, but we do want to use it
# by default for local development, because it greatly speeds up repeated
# test runs.
if [ -n "${NO_VOLUME_MOUNT}" ]; then
    echo "Running tests without volume mount"
    docker run --entrypoint /app/scripts/test-entrypoint.sh --rm balrogagenttest
else
    echo "Running tests with volume mount"
    docker run --entrypoint /app/scripts/test-entrypoint.sh --rm -v `pwd`:/app balrogagenttest
fi
