set -xe
if [ ! -e /app/.cache/mysql/db.done ]; then
    sleep 30
    echo "Initializing DB..."
    python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@balrogdb/balrog create
    mysql -h balrogdb -u balrogadmin --password=balrogadmin balrog < /app/scripts/sample-data.sql
    mysql -h balrogdb -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"balrogadmin\", \"admin\", 1)" balrog
    touch /app/.cache/mysql/db.done
    echo "Done"
fi

# run the command passed from docker
$@
