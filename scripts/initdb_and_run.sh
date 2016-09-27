set -xe

if [ ! -e /app/.cache/mysql/db.done ]; then
    sleep 30
    echo "Initializing DB..."
    python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@balrogdb/balrog create
    bunzip2 -c /app/scripts/sample-data.sql.bz2 | mysql -h balrogdb -u balrogadmin --password=balrogadmin balrog
    mysql -h balrogdb -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"balrogadmin\", \"admin\", 1)" balrog
    touch /app/.cache/mysql/db.done
    echo "Done"
else
    python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@balrogdb/balrog upgrade
fi

# run the command passed from docker
/app/scripts/run.sh $@
