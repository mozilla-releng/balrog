#!/bin/bash

if [ $# -ne 4 ]; then
    echo "Usage: $0 python-interpreter snippet-dir database-uri aus-repo-clone"
    exit 1
fi

PYTHON=$1
SNIPPET_DIR=$2
DBURI=$3
AUS_REPO=$4

PRODUCT=Firefox
BRANCH=mozilla-central
VERSION=10.0a1

export PYTHONPATH=$AUS_REPO

current=`ls $SNIPPET_DIR/$BRANCH/WINNT_x86-msvc | tail -n1`
previous=`ls $SNIPPET_DIR/$BRANCH/WINNT_x86-msvc | tail -n2 | head -n1`

cd $SNIPPET_DIR
for release in $PRODUCT-$BRANCH-nightly-$current $PRODUCT-$BRANCH-nightly-latest; do
    $PYTHON $AUS_REPO/generate-json.py -w $BRANCH -n $release \
            -v $VERSION -p $PRODUCT-$BRANCH-nightly-$previous \
            --db $DBURI --product $PRODUCT
done
