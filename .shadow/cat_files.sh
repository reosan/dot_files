#!/bin/bash
set -e
if [[ $# != 2 ]]; then
    echo "Usage: $0 file comment"
    exit 1
fi

comment() {
    local i end
    end=10
    for i in $(seq 1 $end)
    do
	echo -n $1
    done
    if [[ -n $2 ]]; then
	echo -n " "$2" "
    fi
    for i in $(seq 1 $end)
    do
	echo -n $1
    done
    echo
    echo
}    

DIRS='Arch fedora ubuntu'
FILE=$1
FILE_NAME=$(echo $1 | sed 's@/@\.@g')
COMMENT=$2

if [[ -f ./$FILE ]]; then
    echo "already exists $FILE !"
    exit 2
fi

touch $FILE_NAME
for DIR in $DIRS; do
    comment $COMMENT $DIR >> $FILE_NAME
    if [[ -f $DIR/$FILE ]]; then
	cat $DIR/$FILE >> $FILE_NAME
    else
	echo "$DIR: not exist <$FILE>"
    fi
    comment $COMMENT >> $FILE_NAME
done
