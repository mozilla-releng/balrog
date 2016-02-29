#!/bin/bash

dockerhub_email=bhearsum+test@gmail.com
dockerhub_username=bhearsumtest
dockerhub_password=$(curl taskcluster/secrets/repo:github.com/mozilla/balrog:dockerhub | python -c 'import json, sys; a = json.load(sys.stdin); print a["dockerhub_password"]')

if [ -z $dockerhub_password ]; then
    echo "Dockerhub password not set, can't continue!"
    exit 1
fi

# TODO: create version.json
# TODO: how can uninsntalled versions of library use version.json? maybe a stub one in the repo?

docker build -t bhearsumtest/balrog:latest .
docker login -e $dockerhub_email -u $dockerhub_username -p $dockerhub_password
docker push bhearsumtest/balrog:latest
