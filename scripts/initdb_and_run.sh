set -xe

export LOCAL_DUMP="/app/scripts/prod_db_dump.sql"

if [ ! -e /app/$CACHEDIR/mysql/db.done ]; then
    echo "Initializing DB..."
    python scripts/get-prod-db-dump.py

    xz -d -c $LOCAL_DUMP | mysql -h $DB_HOST -u balrogadmin --password=balrogadmin balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"balrogadmin\", \"admin\", 1)" balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, options, data_version) values (\"balrogagent\", \"scheduled_change\", \"{"actions": ["enact"]}\", 1)" balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e "insert into user_roles (username, role, data_version) values (\"balrogadmin\", \"releng\", 1)" balrog
    touch /app/$CACHEDIR/mysql/db.done
    echo "Done"

fi

# We need to try upgrading even if the database was freshly created, because it
# may use sample data from an older version.
python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@$DB_HOST/balrog upgrade

# run the command passed from docker
/app/scripts/run.sh $@
