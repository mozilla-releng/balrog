#!/bin/bash

pip install -r /app/requirements-test.txt
tox $@
