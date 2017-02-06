#!/bin/bash
# PROMPT_COMMAND="$(echo -n \
# 	'printf \"\e[?25l\";' \
# 	'pc=$?;' \
# 	'WD_COL_NUM=$(pwd | wc -m);' \
# 	'printf' \
# 	$(IFS=$'\n'; echo_cat $(for i in \
# 		\"'\" \
# 		'\e[s' \
# 		'\e[1;$(expr $COLUMNS - ${WD_COL_NUM} + 1)f' \
# 		'$(for n in $(seq 1 ${WD_COL_NUM});' \
# 		'do ' \
# 			'echo -n \" \";' \
# 		'done)' \
# 		'\e[${WD_COL_NUM}D' \
# 		'\e[1m$(PWD)\e[0m\n' \
# 		'\e[$(expr $COLUMNS - 11)C' \
# 		'$(LANG=en_US.UTF-8 date +\"%a %b %d\")\n' \
# 		'\e[$(expr $COLUMNS - 6)C' \
# 		'$(TZ=\"Asia/Tokyo\" date +\"%H:%M\")' \
# 		'\e[u' \
# 		\"'\" \
# 		';' \
# 		do \
# 			echo $i \
# 		done \
# 	)) \
# 	'printf \"\e[?25h\"' \
# )"


echo_cat() {
    local ret
    for tmp in $*
    do
	ret+=$tmp
    done
    echo -n $ret
}

PROMPT_COMMAND=$(echo -n \
	'printf "\033[?25l";' \
	'pc=$?;' \
	'WD_COL_NUM=$(pwd | wc -m);' \
	'printf' \
	$(IFS=$'\n'; echo_cat $(for i in \
		'"' \
		'\033[s' \
		'\033[1;$(($COLUMNS-${WD_COL_NUM}+1))f' \
		'$(for n in $(seq 1 ${WD_COL_NUM});' \
		'do ' \
			'echo -n '"'"' '"'"';' \
		'done)' \
		'\033[${WD_COL_NUM}D' \
		'\033[1m${PWD}\e[0m\n' \
		'\033[$(($COLUMNS-11))C' \
		'$(LANG=en_US.UTF-8 date +'"'"'%a %b %d'"'"')\n' \
		'\033[$(($COLUMNS-6))C' \
		'$(TZ=Asia/Tokyo date +'"'"'%H:%M'"'"')' \
		'\033[u' \
		'"' \
		';'
		do
			echo $i
		done
	)) \
	'printf "\033[?25h"' \
)

eval $PROMPT_COMMAND

