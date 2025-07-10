#!/bin/bash
# This runs in docker to pin our requirements files.
set -x
set -e
SUFFIX=${SUFFIX:-txt}
if [ $# -gt 0 ]; then
    EXTRA_PCM_ARGS="$@"
fi

PIP="pip --disable-pip-version-check install --root-user-action ignore"
$PIP --upgrade 'pip<25.1'
$PIP 'pip-compile-multi<3' 'uv'

apt-get update

# --backtracing is required to work around issues with pyjwt, eg:
# Using legacy resolver. Consider using backtracking resolver with `--resolver=backtracking`.
# Could not find a version that matches pyjwt[crypto]==2.4.0,>=2.6.0 from https://files.pythonhosted.org/packages/1c/fb/b82e9601b00d88cf8bbee1f39b855ae773f9d5bcbcedb3801b2f72460696/PyJWT-2.4.0-py3-none-any.whl (from -r requirements/base.in (line 29))
# --allow-unsafe is required because local dev environments need all deps hashed to install properly
ARGS="-g base -g docs -g test -g local --backtracking --allow-unsafe"
pip-compile-multi --uv -o "$SUFFIX" $ARGS $EXTRA_PCM_ARGS
chmod 644 requirements/*.txt

cd agent
ARGS="-g base -g test -g local --backtracking --allow-unsafe"
pip-compile-multi --uv -o "$SUFFIX" $ARGS $EXTRA_PCM_ARGS
chmod 644 requirements/*.txt
