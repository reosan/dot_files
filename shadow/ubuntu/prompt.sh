#!/bin/sh
trap 'printf "\e[0m"' DEBUG
export TZ=Tokyo
pc=$?
wd=$(pwd | wc -m) # Working Directory
pd=$(pwd | wc -m) # Past Directory
PROMPT_COMMAND='pc=$?; wd=$(pwd | wc -m); printf "\e[s\e[1;$(expr $COLUMNS - ${pd} + 1)f$(for n in $(seq 1 ${pd});do printf " ";done)\e[${wd}D\e[1m$(pwd)\e[0m\n\e[$(expr $COLUMNS - 11)C$(LANG=en_US.UTF-8 date +"%a %b %d")\n\e[$(expr $COLUMNS - 6)C$(TZ="Asia/Tokyo" date +"%H:%M")\e[u"; pd=$(pwd | wc -m)'
PS1='\[\e[0m\]$pc $SHLVL $(if [ $pc -eq 0 ]; then echo "\[\e[0;32m\];)"; else echo "\[\e[0;31m\]:("; fi) \[\e[38;5;248m\]\W \[\e[0;34m\]\$ \[\e[38;5;248m\]'

colors() {
    local fgc bgc vals seq0

    printf "Color escapes are %s\n" '\e[${value};...;${value}m'
    printf "Values 30..37 are \e[33mforeground colors\e[m\n"
    printf "Values 40..47 are \e[43mbackground colors\e[m\n"
    printf "Value  1 gives a  \e[1mbold-faced look\e[m\n\n"

    # foreground colors
    for fgc in {30..37}; do
	# background colors
	for bgc in {40..47}; do
	    fgc=${fgc#37} # white
	    bgc=${bgc#40} # black

	    vals="${fgc:+$fgc;}${bgc}"
	    vals=${vals%%;}

	    seq0="${vals:+\e[${vals}m}"
	    printf "  %-9s" "${seq0:-(default)}"
	    printf " ${seq0}TEXT\e[m"
	    printf " \e[${vals:+${vals+$vals;}}1mBOLD\e[m"
	done
	echo; echo
    done
}

colors256() {
    ~/Programs/256colors
}
