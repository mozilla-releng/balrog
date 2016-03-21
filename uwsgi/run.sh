#!/bin/bash

if [ $1 == "public" ]; then
   exec uwsgi --ini /app/uwsgi/public.ini --python-autoreload 1
elif [ $1 == "admin" ]; then
   exec uwsgi --ini /app/uwsgi/admin.ini --python-autoreload 1
elif [ $1 == "admin-dev" ]; then
   exec uwsgi --ini /app/uwsgi/admin.dev.ini --ini /app/uwsgi/admin.ini --python-autoreload 1
else
   echo "unknown mode: $1"
   exit 1
fi
