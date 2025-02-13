#!/bin/sh
set -e

test $APP
test $APP_VERSION
test $DOCKER_REPO
test $MOZ_FETCHES_DIR
test $TASKCLUSTER_ROOT_URL
test $TASK_ID
test $VCS_HEAD_REPOSITORY
test $VCS_HEAD_REV

echo "=== Generating dockercfg ==="
PASSWORD_URL=http://taskcluster/secrets/v1/secret/repo:github.com/mozilla-releng/balrog:dockerhub
mkdir -m 700 $HOME/.docker
curl $PASSWORD_URL | jq '.secret.dockercfg' > $HOME/.docker/config.json
chmod 600 $HOME/.docker/config.json


cd $MOZ_FETCHES_DIR
unzstd image.tar.zst

echo "=== Inserting version.json into image ==="
# Create an OCI copy of image in order umoci can patch it
skopeo copy docker-archive:image.tar oci:balrog${APP}:final

cat > version.json <<EOF
{
    "commit": "${VCS_HEAD_REV}",
    "version": "${APP_VERSION}",
    "source": "${VCS_HEAD_REPOSITORY}",
    "build": "${TASKCLUSTER_ROOT_URL}/tasks/${TASK_ID}"
}
EOF

umoci insert --image balrog${APP}:final version.json /app/version.json

echo "=== Pushing to docker hub ==="
DOCKER_TAG="v${APP_VERSION}"
skopeo copy oci:balrog${APP}:final docker://$DOCKER_REPO:$DOCKER_TAG
skopeo inspect docker://$DOCKER_REPO:$DOCKER_TAG

echo "=== Clean up ==="
rm -rf $HOME/.docker
