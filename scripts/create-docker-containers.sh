#!/bin/bash

balrog_repo=$(dirname $(dirname $(realpath $0)))

which docker &>/dev/null
if [ "$?" != "0" ]; then
    echo "Docker binary not found, cannot proceed!"
    exit 1
fi

echo "Balrog repo is $balrog_repo"

docker ps -a | grep -q balrog-database
if [ "$?" == "0" ]; then
    echo "balrog-database container already exists, skipping..."
else
    echo "Creating balrog-database container..."
    docker create --net host -e MYSQL_DATABASE=balrog -e MYSQL_USER=balrogadmin -e MYSQL_PASSWORD=balrogadmin -e MYSQL_ROOT_PASSWORD=admin --name balrog-database -v /var/lib/mysql -it mysql:5.7
    echo "Initializing database..."
    docker start balrog-database
    # Wait for the database to come up
    sleep 30
    docker run --rm --net host -it bhearsum/balrog:latest python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@127.0.0.1/balrog create
    docker run --rm --net host -it bhearsum/balrog:latest sh -c 'exec mysql -h 127.0.0.1 -P 3306 -u balrogadmin --password=balrogadmin balrog < sample-data.sql'
    docker run --rm --net host -it bhearsum/balrog:latest sh -c 'exec mysql -h 127.0.0.1 -P 3306 -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"balrogadmin\", \"admin\", 0);" balrog'
fi

docker ps -a | grep -q balrog-admin
if [ "$?" == "0" ]; then
    echo "balrog-admin container already exists, skipping..."
else
    echo "Creating balrog-admin container..."
    docker create --net host -e DBURI=mysql://balrogadmin:balrogadmin@127.0.0.1/balrog -e SECRET_KEY=blahblah --name balrog-admin -v `pwd`:/app -it bhearsum/balrog:latest uwsgi --ini /app/uwsgi/admin.ini
    docker start balrog-admin
fi

docker ps -a | grep -q balrog-public
if [ "$?" == "0" ]; then
    echo "balrog-public container already exists, skipping..."
else
    echo "Creating balrog-public container..."
    docker create --net host -e DBURI=mysql://balrogadmin:balrogadmin@127.0.0.1/balrog --name balrog-public -v `pwd`:/app -it bhearsum/balrog:latest uwsgi --ini /app/uwsgi/public.ini
    docker start balrog-public
fi
