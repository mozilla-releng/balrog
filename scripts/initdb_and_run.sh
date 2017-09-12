set -xe

export LOCAL_DUMP="/app/scripts/prod_db_dump.sql"

if [ ! -e /app/.cache/mysql/db.done ]; then
    echo "Initializing DB..."
    python scripts/get-prod-db-dump.py

    cat $LOCAL_DUMP | mysql -h balrogdb -u balrogadmin --password=balrogadmin balrog
    mysql -h balrogdb -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"balrogadmin\", \"admin\", 1)" balrog
    mysql -h balrogdb -u balrogadmin --password=balrogadmin -e "insert into user_roles (username, role, data_version) values (\"balrogadmin\", \"releng\", 1)" balrog
    touch /app/.cache/mysql/db.done
    echo "Done"

fi

# We need to try upgrading even if the database was freshly created, because it
# may use sample data from an older version.
python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@balrogdb/balrog upgrade

# run the command passed from docker
/app/scripts/run.sh $@
