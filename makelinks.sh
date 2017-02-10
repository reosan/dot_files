#!/bin/bash
foo="$HOME/foo"
CD=$(pwd)
DIRS=$(find . -type d)
FILES=$(find . -type f)
# FILES=$(find . !  -type d -a ! -type l -a ! -type -a ! -type D -a ! -type s -a ! -type p -a ! -type c -a ! -type b )) 
FILES=$(echo -e "$FILES" | grep -vF -f <(echo -e "$DIRS" | sed -r 's/\./\\./g'))
FILES=$(echo -e "$FILES" | grep -vE '^\./\.(git|shadow)')
LINKS=$(echo -e "$FILES" | sed -r "s@(^\./)(.)@\1\.\2@"| sed -r "s@^\.@$foo@")
DIRS=$(echo -e "$DIRS" | grep -Ev '\.+($|/\..*)' | sed -r "s@(^\./)(.)@\1\.\2@"| sed -r "s@^\.@$foo@")
FILES=$(echo -e "$FILES" | sed -r "s@^\.@$CD@")

FILES=$(echo -e "$FILES" | grep -Ev $CD'/(README\.md|makelinks\.sh)')
LINKS=$(echo -e "$LINKS" | grep -Ev $foo'/\.(README\.md|makelinks\.sh)')
echo
echo 'DIRS:'
echo -e "$DIRS"
echo
echo 'FILES	LINKS'
diff --side-by-side <(echo -e "$FILES") <(echo -e "$LINKS")
echo

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
    echo -n '$?='"$?"" "
    echo $n"/"$lines
done < <(paste -d $'\t' <(echo -e "$FILES") <(echo -e "$LINKS"))

