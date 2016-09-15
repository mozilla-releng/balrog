#!/bin/bash

build_front_end() {
    cd /app/ui
    npm install
    npm run build
    cd -
}


if [ $1 == "public" ]; then
   exec uwsgi --ini /app/uwsgi/public.ini --python-autoreload 1
elif [ $1 == "admin" ]; then
   exec uwsgi --ini /app/uwsgi/admin.ini --python-autoreload 1
elif [ $1 == "admin-dev" ]; then
    # When running the dev instance, we override /app by the developer's folder on his host
    # machine. Building the frontend here makes sure we always serve the most up to date
    # revision at each `docker-compose up`. You can still build it manually with, though
    build_front_end

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
else
   echo "unknown mode: $1"
   exit 1
fi
