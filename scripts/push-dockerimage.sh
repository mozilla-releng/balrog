#!/bin/bash

set -e

tags=$@

password_url="taskcluster/secrets/v1/secret/repo:github.com/mozilla/balrog:dockerhub"
artifact_url="taskcluster/queue/v1/task/${TASK_ID}/runs/${RUN_ID}/artifacts/public/docker-image-shasum256.txt"
artifact_expiry=$(date -d "+1 year" -u +%FT%TZ)
dockerhub_email=release+balrog@mozilla.com
dockerhub_username=mozillabalrog
dockerhub_password=$(curl ${password_url} | python -c 'import json, sys; a = json.load(sys.stdin); print a["secret"]["dockerhub_password"]')

if [ -z $dockerhub_password ]; then
    echo "Dockerhub password not set, can't continue!"
    exit 1
fi
if [ ${#tags[@]} -eq 0 ]; then
    echo "Must pass at least one tag"
    exit 2
fi

commit=$(git rev-parse HEAD)
version=$(cat version.txt)

cat > version.json <<EOF
{
    "commit": "${commit}",
    "version": "${version}",
    "source": "https://github.com/mozilla/balrog",
    "build": "https://tools.taskcluster.net/task-inspector/#${TASK_ID}"
}
EOF

echo "Building Docker image"
docker build -t buildtemp .
echo "Logging into Dockerhub"
docker login -e $dockerhub_email -u $dockerhub_username -p $dockerhub_password

for tag in ${tags[@]}; do
    echo "Tagging Docker image with ${tag}"
    docker tag buildtemp "mozilla/balrog:${tag}"
    echo "Pushing Docker image tagged with ${tag}"
    docker push mozilla/balrog:${tag}
done

sha256=$(docker images --no-trunc mozilla/balrog | grep "${tags[0]}" | awk '/^mozilla/ {print $3}')
echo "SHA256 is ${sha256}, creating artifact for it"
put_url=$(curl --retry 5 --retry-delay 5 --data "{\"storageType\": \"s3\", \"contentType\": \"text/plain\", \"expires\": \"${artifact_expiry}\"}" ${artifact_url} | python -c 'import json; import sys; print json.load(sys.stdin)["putUrl"]')
curl --retry 5 --retry-delay 5 -X PUT -H "Content-Type: text/plain" --data "${sha256}" "${put_url}"
echo 'Artifact created, all done!'
