#!/bin/bash

run_back_end_tests() {
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
  backend_rc=$?
  run_front_end_tests
  frontend_rc=$?
  echo 

  if [[ $backend_rc == 0 && $frontend_rc == 0 ]]; then
    echo "All tests pass!!!"
    exit 0
  else
    echo "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL. See above for details."
    exit 1
  fi
fi
