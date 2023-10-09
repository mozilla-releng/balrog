set -x

export LOCAL_DUMP="/app/scripts/prod_db_dump.sql"

mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'show tables;' balrog | grep rules
rc=$?
if [ "$rc" -eq 1 ]; then
    echo "Initializing DB..."
    python scripts/get-prod-db-dump.py

    xz -d -c $LOCAL_DUMP | mysql -h $DB_HOST -u balrogadmin --password=balrogadmin balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'insert into permissions (username, permission, options, data_version) values ("balrogagent", "scheduled_change", "{\"actions\": [\"enact\"]}", 1)' balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'insert into permissions (username, permission, options, data_version) values ("bob@mozilla.com", "release", "{\"actions\": [\"get\"]}", 1)' balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'insert into permissions (username, permission, options, data_version) values ("janet@mozilla.com", "release", "{\"actions\": [\"get\"]}", 1)' balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'insert into user_roles (username, role, data_version) values ("bob@mozilla.com", "releng", 1);' balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'insert into user_roles (username, role, data_version) values ("janet@mozilla.com", "releng", 1);' balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e 'insert into product_req_signoffs (product, channel, role, signoffs_required, data_version) values ("Firefox", "release", "releng", 1, 1);' balrog
    echo "Done"
fi

# We need to try upgrading even if the database was freshly created, because it
# may use sample data from an older version.
python scripts/manage-db.py -d mysql://balrogadmin:balrogadmin@$DB_HOST/balrog upgrade

# run the command passed from docker
/bin/bash /app/scripts/run.sh $@
