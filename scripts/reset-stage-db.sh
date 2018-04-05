#!/bin/bash
set -e
set -x

export LOCAL_DUMP="/app/scripts/prod_db_dump.sql"

DBURI=$1
MAGIC_WORD=$2

# This operation is destructive, we must ensure we never run it in prod
echo "Performing sanity check..."
if [[ $ENV != "stage" || $MAGIC_WORD != "destroythedatabase" ]]
then
  echo "Not in stage environment (found \"${ENV}\" in \$ENV, and \"${MAGIC_WORD}\" as the magic word), cannot proceed"
  exit 1
fi

# Because the "mysql" command doesn't accept URIs...
username=$(python -c "import urlparse; result = urlparse.urlparse('${DBURI}'); print result.netloc.split('@')[0].split(':')[0]")
password=$(python -c "import urlparse; result = urlparse.urlparse('${DBURI}'); print result.netloc.split('@')[0].split(':')[1]")
host=$(python -c "import urlparse; result = urlparse.urlparse('${DBURI}'); print result.netloc.split('@')[-1]")
database=$(python -c "import urlparse; result = urlparse.urlparse('${DBURI}'); print result.path.lstrip('/')")

echo -n "Proceeding with reset of $database on $host in "
for i in `seq 10 -1 1`; do echo -n $i... && sleep 1; done
echo

# Because the production database dumps contain no permissions, we need to
# make sure we maintain stage's permissions, otherwise automation will not
# work after the reset has been completed.
echo "Backing up existing permissions, roles, and required signoffs..."
mysqldump --skip-add-drop-table --no-create-info -h "$host" -u "$username" --password="$password" "$database" permissions user_roles product_req_signoffs permissions_req_signoffs > backup.sql
cat backup.sql

echo "Download prod dump..."
python scripts/get-prod-db-dump.py

echo "Overriding current database with production dump..."
xz -d -c $LOCAL_DUMP | mysql -h "$host" -u "$username" --password="$password" "$database"

echo "Upgrading database to the latest version..."
python scripts/manage-db.py -d $DBURI upgrade

echo "Re-adding permissions, roles, and required signoffs..."
cat backup.sql
cat backup.sql | mysql -h "$host" -u "$username" --password="$password" "$database"
mysqldump --skip-add-drop-table --no-create-info -h "$host" -u "$username" --password="$password" "$database" permissions user_roles product_req_signoffs permissions_req_signoffs
