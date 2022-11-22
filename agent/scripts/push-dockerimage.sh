#!/bin/bash

set -e

tags=( $@ )

password_url="taskcluster/secrets/v1/secret/repo:github.com/mozilla-releng/balrog:dockerhub"
artifact_url="taskcluster/queue/v1/task/${TASK_ID}/runs/${RUN_ID}/artifacts/public/docker-image-shasum256.txt"
artifact_expiry=$(date -d "+1 year" -u +%FT%TZ)

if [ ${#tags[*]} -eq 0 ]; then
    echo "Must pass at least one tag"
    exit 2
fi

commit=$(git rev-parse HEAD)
version=$(cat version.txt)

apt-get update || :
apt-get -y install jq

cat > version.json <<EOF
{
    "commit": "${commit}",
    "version": "${version}",
    "source": "https://github.com/mozilla-releng/balrog",
    "build": "https://firefox-ci-tc.services.mozilla.com/tasks/${TASK_ID}"
}
EOF

echo "Building Docker image"
docker build -t buildtemp .
# docker login stopped working in Taskcluster for some reason
wget -qO- $password_url | jq '.secret.dockercfg' > /root/.dockercfg
chmod 600 /root/.dockercfg

for tag in ${tags[*]}; do
    echo "Tagging Docker image with ${tag}"
    docker tag buildtemp "mozilla/balrogagent:${tag}"
    echo "Pushing Docker image tagged with ${tag}"
    docker push mozilla/balrogagent:${tag}
done

sha256=$(docker images --no-trunc mozilla/balrogagent | grep "${tags[0]}" | awk '/^mozilla/ {print $3}')
echo "SHA256 is ${sha256}, creating artifact for it"
put_url=$(curl --retry 5 --retry-delay 5 --data "{\"storageType\": \"s3\", \"contentType\": \"text/plain\", \"expires\": \"${artifact_expiry}\"}" ${artifact_url} | python -c 'import json; import sys; print json.load(sys.stdin)["putUrl"]')
curl --retry 5 --retry-delay 5 -X PUT -H "Content-Type: text/plain" --data "${sha256}" "${put_url}"
echo 'Artifact created, all done!'

