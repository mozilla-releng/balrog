#!/bin/sh

# deletes are required to be done in small batches since they take
# too long to do as one large DB transaction

cd $(dirname $0)
if [ $# -ne 3 ]; then
    echo "Usage: $0 DBURI MAX_AGE <length in seconds>"
    echo "Example: $0 <dburi> <maxage> 21600 -- runs for 6 hours"
    echo " -- this script runs batch deletes in a loop for the time specified"
    exit 1
fi

DBURI=$1
MAX_AGE=$2

START=$(date '+%s')
TIL=$(expr $START + $3)

TOTAL=0
while true; do
    NOW=$(date '+%s')
    if [ $NOW -gt $TIL ]; then
        break
    fi

    printf "Deleting..."
    # DBURI and MAX_AGE should be in the environment
    DELETED=$(python ./manage-db.py -d "$DBURI" cleanup "$MAX_AGE" 2>/dev/null)
    if ! [ "$?" -eq "0" ]; then
        echo "manage-db.py didn't exit cleanly"
        continue
    fi
    DELETED=$(echo "$DELETED" | awk '/Total/ {print $3}')
    ORIG_DELETED=$DELETED
    # Sometimes DELETED ends up not being set for some reason, which breaks
    # the `expr` expressions below, and gets the script stuck in a loop.
    if ! [ "$DELETED" -eq "$DELETED" ] 2>/dev/null; then
        DELETED=0
    fi
    TOTAL=$(expr $TOTAL + $DELETED)
    NOW=$(date '+%s')
    printf "%d rows removed >>> %d seconds remaining. %d deleted.\n" $DELETED $(expr $TIL - $NOW) $TOTAL

    echo "Original value for \$DELETED: $ORIG_DELETED"
    if [ $DELETED -eq 0 ]; then
        echo "Nothing left to do"
        exit 0
    fi
done
