#!/bin/bash
# This runs in docker to pin our requirements files.
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
chmod 644 requirements/*.txt
