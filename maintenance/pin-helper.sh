#!/bin/bash
# This runs in docker to pin our requirements files.
set -x
set -e
SUFFIX=${SUFFIX:-txt}
if [ $# -gt 0 ]; then
    EXTRA_PCM_ARGS="$@"
fi

pip install --upgrade pip
pip install pip-compile-multi

apt-get update

ARGS="-g base -g docs -g test -g local"
pip-compile-multi -o "$SUFFIX" $ARGS $EXTRA_PCM_ARGS
sed -i 's/^repoze-lru/repoze.lru/' requirements/*.txt
chmod 644 requirements/*.txt

cd agent
ARGS="-g base -g test -g local"
pip-compile-multi -o "$SUFFIX" $ARGS $EXTRA_PCM_ARGS
chmod 644 requirements/*.txt
