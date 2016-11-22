set -xe

if [ ! -e /app/.cache/mysql/db.done ]; then
    # We need to sleep awhile for fresh databases because mysql will take longer to initialize.
    # Ideally, this would find some better way to probe for mysql-readyness.
    sleep 45
    echo "Initializing DB..."
    python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@balrogdb/balrog create
    bunzip2 -c /app/scripts/sample-data.sql.bz2 | mysql -h balrogdb -u balrogadmin --password=balrogadmin balrog
    mysql -h balrogdb -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"balrogadmin\", \"admin\", 1)" balrog
    touch /app/.cache/mysql/db.done
    echo "Done"
else
    # We also should sleep for existing databases, but we don't need for nearly as long.
    sleep 10
fi

# We need to try upgrading even if the database was freshly created, because it
# may use sample data from an older version.
python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@balrogdb/balrog upgrade

# run the command passed from docker
/app/scripts/run.sh $@
