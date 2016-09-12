#!/bin/bash

run_back_end_tests() {
  pip install -r /app/requirements-test.txt
  tox $@
}

run_front_end_tests() {
  cd ui/
  npm test
}

type_of_tests="$1"

if [[ $type_of_tests == "backend" ]]; then
  shift
  run_back_end_tests $@
elif [[ $type_of_tests == "frontend" ]]; then
  run_front_end_tests
else
  run_back_end_tests $@
  run_front_end_tests
fi
