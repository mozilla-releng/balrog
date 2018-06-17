#!/bin/bash
PYTHON_VERSION="py27"

build_front_end() {
    cd /app/ui
    npm install
    npm run build
    cd -
}

run_back_end_tests() {
  PYTHON_VERSION=${1:-py27}
  shift
  cd /app
  tox $@ -e $PYTHON_VERSION
}

run_front_end_tests() {
  build_front_end
  cd /app/ui/
  npm test
}

if [ $1 == "public" ]; then
   exec uwsgi --ini /app/uwsgi/public.ini --python-autoreload 1
elif [ $1 == "admin" ]; then
   exec uwsgi --ini /app/uwsgi/admin.ini --python-autoreload 1
elif [ $1 == "admin-dev" ]; then
    exec uwsgi --ini /app/uwsgi/admin.dev.ini --ini /app/uwsgi/admin.ini --python-autoreload 1
elif [ $1 == "create-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    exec python scripts/manage-db.py -d ${DBURI} create
elif [ $1 == "upgrade-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    exec python scripts/manage-db.py -d ${DBURI} upgrade
elif [ $1 == "cleanup-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    if [ -z "${MAX_AGE}" ]; then
        echo "\${MAX_AGE} must be set!"
        exit 1
    fi
    if [ -z "${DELETE_RUN_TIME}" ]; then
        echo "\${DELETE_RUN_TIME} must be set!"
        exit 1
    fi

    exec scripts/run-batch-deletes.sh $DBURI $MAX_AGE $DELETE_RUN_TIME
elif [ $1 == "extract-active-data" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    if [ -z "${OUTPUT_FILE}" ]; then
        echo "\${OUTPUT_FILE} must be set!"
        exit 1
    fi
    python scripts/manage-db.py -d ${DBURI} extract dump.sql
    xz -T0 -zc dump.sql > ${OUTPUT_FILE}
elif [ $1 == "reset-stage-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    if [ -z "${2}" ]; then
        echo "magic word must be passed as second positional argument"
        exit 1
    fi
    exec scripts/reset-stage-db.sh $DBURI $2
elif [ $1 == "test" ]; then
    shift
    rc=0
    coveralls=0
    if [[ $1 == "backend" ]]; then
        shift
        coveralls=1
        run_back_end_tests $@
        rc=$?
    elif [[ $1 == "frontend" ]]; then
        run_front_end_tests
        rc=$?
    else
        coveralls=1
        run_back_end_tests $@
        backend_rc=$?
        run_front_end_tests
        frontend_rc=$?
        echo

        if [[ $backend_rc == 0 && $frontend_rc == 0 ]]; then
            echo "All tests pass!!!"
            exit 0
        else
            echo "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL. Some tests failed, see above for details."
            exit 1
        fi
    fi
    # Only send coverage data for the authoritative Balrog repo.
    if [[ $PYTHON_VERSION == "py27" && $coveralls == 1 && $GITHUB_BASE_REPO_URL == "https://github.com/mozilla/balrog.git" ]];
    then
        # COVERALLS_REPO_TOKEN is already in the environment
        export CIRCLECI=1
        export CI_PULL_REQUEST=$GITHUB_PULL_REQUEST
        cd /app
        coveralls
    fi
    exit $rc
else
   echo "unknown mode: $1"
   exit 1
fi
