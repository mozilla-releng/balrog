#!/bin/bash

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
    exec python scripts/manage-db.py -d ${DBURI} cleanup-dryrun ${MAX_AGE}
else
   echo "unknown mode: $1"
   exit 1
fi
