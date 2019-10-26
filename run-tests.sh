#!/bin/bash

# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
docker build -t balrogtest -f Dockerfile.dev .

# When running in Taskcluster, we want to send coverage data. To do that we need the repo token
# that is stored in the Secrets Service. We cannot access that from within the test container,
# so we must do it here, and that pass it in
COVERALLS_REPO_TOKEN=""
if [[ $GITHUB_BASE_REPO_URL == "https://github.com/mozilla/balrog.git" ]];
then
    password_url="taskcluster/secrets/v1/secret/repo:github.com/mozilla/balrog:coveralls"
    repo_token=$(curl ${password_url} | python -c 'import json, sys; a = json.load(sys.stdin); print a["secret"]["repo_token"]')
    export COVERALLS_REPO_TOKEN=$repo_token
fi
# We can't use a volume mount in Taskcluster, but we do want to use it
# by default for local development, because it greatly speeds up repeated
# test runs.
if [ -n "${NO_VOLUME_MOUNT}" ]; then
    echo "Running tests without volume mount"
    docker run -e GITHUB_BASE_REPO_URL=$GITHUB_BASE_REPO_URL -e GITHUB_PULL_REQUEST=$GITHUB_PULL_REQUEST -e COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN --rm balrogtest test $@
else
    echo "Running tests with volume mount"
    docker run -e GITHUB_BASE_REPO_URL=$GITHUB_BASE_REPO_URL -e GITHUB_PULL_REQUEST=$GITHUB_PULL_REQUEST -e COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN --rm -v balrog-tox:/app/.tox balrogtest test $@
fi
