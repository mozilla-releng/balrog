#!/bin/bash

if [ $1 == "agent" ]; then
    exec /usr/local/bin/python -m balrogagent.cmd
elif [ $1 == "version" ]; then
    cat version.json
fi
