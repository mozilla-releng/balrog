#!/bin/bash

set -e

extra_tag=$1

password_url="taskcluster/secrets/v1/secret/repo:github.com/testbhearsum/balrog:dockerhub"
artifact_url="taskcluster/queue/v1/task/${TASK_ID}/runs/${RUN_ID}/artifacts/public/docker-image-shasum256.txt"
artifact_expiry=$(date -d "+1 year" -u +%FT%TZ)
dockerhub_email=bhearsum+test@mozilla.com
dockerhub_username=bhearsumtesttest
dockerhub_password=$(curl ${password_url} | python -c 'import json, sys; a = json.load(sys.stdin); print a["secret"]["dockerhub_password"]')

if [ -z $dockerhub_password ]; then
    echo "Dockerhub password not set, can't continue!"
    exit 1
fi

commit=$(git rev-parse HEAD)
version=$(cat version.txt)
# This is hardcoded because we can't accurately set it programatically for
# release events, where we've updated to a tag. At the time of writing,
# we only built docker images for commits to master or release events...
branch=master
#branch=$(git rev-parse --abbrev-ref HEAD)
date=$(date --utc +%Y-%m-%d-%H-%M)

echo "{
    \"commit\": \"${commit}\",
    \"version\": \"${version}\",
    \"source\": \"https://github.com/testbhearsum/balrog\",
    \"build\": \"https://tools.taskcluster.net/task-inspector/#${TASK_ID}\"
}" > version.json

# Initialize and update the UI submodule
git submodule init
git submodule update

branch_tag="${branch}"
if [ "$branch" == "master" ]; then
    branch_tag="latest"
fi
date_tag="${branch}-${date}"
commit_tag="${branch}-${commit}"

echo "Building Docker image"
docker build -t bhearsumtesttest/balrogagent:${branch_tag} .
echo "Tagging Docker image with date tag"
docker tag bhearsumtesttest/balrogagent:${branch_tag} "bhearsumtesttest/balrogagent:${date_tag}"
echo "Tagging Docker image with git commit tag"
docker tag bhearsumtesttest/balrogagent:${branch_tag} "bhearsumtesttest/balrogagent:${commit_tag}"
echo "Logging into Dockerhub"
docker login -e $dockerhub_email -u $dockerhub_username -p $dockerhub_password
echo "Pushing Docker image"
docker push bhearsumtesttest/balrogagent:${branch_tag}
docker push bhearsumtesttest/balrogagent:${date_tag}
docker push bhearsumtesttest/balrogagent:${commit_tag}

if [ ! -z $extra_tag ]; then
  echo "Tagging Docker image with ${extra_tag}"
  docker tag bhearsumtesttest/balrogagent:${branch_tag} "bhearsumtesttest/balrogagent:${extra_tag}"
  docker push bhearsumtesttest/balrogagent:${extra_tag}
fi

sha256=$(docker images --no-trunc bhearsumtesttest/balrogagent | grep "${date_tag}" | awk '/^bhearsumtesttest/ {print $3}')
echo "SHA256 is ${sha256}, creating artifact for it"
put_url=$(curl --retry 5 --retry-delay 5 --data "{\"storageType\": \"s3\", \"contentType\": \"text/plain\", \"expires\": \"${artifact_expiry}\"}" ${artifact_url} | python -c 'import json; import sys; print json.load(sys.stdin)["putUrl"]')
curl --retry 5 --retry-delay 5 -X PUT -H "Content-Type: text/plain" --data "${sha256}" "${put_url}"
echo 'Artifact created, all done!'
