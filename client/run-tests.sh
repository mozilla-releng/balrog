#!/bin/bash

IMAGE='balrogclient-test'

docker build -t ${IMAGE} -f Dockerfile.dev .

if [ -n "${NO_VOLUME_MOUNT}" ]; then
    echo "Running tests without volume mount"
    docker run --rm ${IMAGE} tox -c /app/tox.ini $@
else
    echo "Running tests with volume mount"
    docker run --rm -v $(pwd):/app ${IMAGE} tox -c /app/tox.ini $@
fi

