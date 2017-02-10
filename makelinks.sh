#!/bin/bash
HOGE="$HOME/hoge"
CD=$(pwd)
DIRS=$(find $CD -type d)
FILES=$(find $CD -type f)

FILES=$(echo -e "$FILES" | grep -vF -f <(echo -e "$DIRS" | sed -r 's/\./\\./g'))
FILES=$(echo -e "$FILES" | grep -vE '^\./\.git')
LINKS=$(echo -e "$FILES" | sed -r "s@(^\./)(.)@\1\.\2@"| sed -r "s@^\.@$HOGE@")
DIRS=$(echo -e "$DIRS" | grep -Ev '\.+($|/\..*)' | sed -r "s@(^\./)(.)@\1\.\2@"| sed -r "s@^\.@$HOGE@")
FILES=$(echo -e "$FILES" | sed -r "s@^\.@$CD@")

for dir in $DIRS
do
    mkdir -p $dir
done

lines=$(echo -e "$LINKS" | wc -l)
n=0
while read file link
do
    n=$(( $n + 1 ))
    ln -fs $file $link
    echo -n "$?"" "
    echo $n"/"$lines
done < <(paste -d $'\t' <(echo -e "$FILES") <(echo -e "$LINKS"))

