#!/bin/bash
set -e
URL_BASE='https://www.forexite.com/free_forex_quotes/'
url='https://www.dukascopy.com/'

if [ $# != 3 ]; then
    echo 'Usage: ./wget_forexite YYYY MM DD'
fi

ZIP_FILE=$3$2$(echo -n $1 | sed -r 's/..(..)/\1/').zip
echo $ZIP_FILE
wget $URL_BASE"$1/$2/$ZIP_FILE"
unzip $ZIP_FILE
/bin/rm $ZIP_FILE
