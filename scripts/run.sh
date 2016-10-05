#!/bin/bash

build_front_end() {
    cd /app/ui
    npm install
    npm run build
    cd -
}

run_back_end_tests() {
  cd /app
  tox $@
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
elif [ $1 == "test" ]; then
    shift
    if [[ $1 == "backend" ]]; then
        shift
        run_back_end_tests $@
    elif [[ $1 == "frontend" ]]; then
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
            echo "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL. Some tests failed, see above for details."
            exit 1
        fi
    fi
else
   echo "unknown mode: $1"
   exit 1
fi
