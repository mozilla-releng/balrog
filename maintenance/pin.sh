#!/usr/bin/env bash
# We run this in balrog/. to pin all requirements.
#
# Usage: maintenance/pin.sh [<extra-pip-compile-multi-arguments>]
#
set -e
set -x

docker run --rm -t -v $PWD:/src -w /src python:3.9 maintenance/pin-helper.sh $@
