#!/bin/bash
# 8 * 18 * 12 -> 72
# 9 * 4  * 6
# 72 * 2 == 144

colors_all() {
    local h i j k t w
    printf "\n"

    t='256-color mode — foreground: ESC[38;5;#m   background: ESC[48;5;#m'
    w=$(echo -n $t | wc -m)
    printf "\033[%dC" $(( (144-$w)/2 ))
    printf "\033[1m"; echo $t; echo; printf "\033[0m"

    t='Standard colors'
    w=$(echo -n $t | wc -m)
    printf "\033[%dC" $(( (72-$w)/2 ))
    echo -n $t; printf "\033[%dC" $(( 72 - (72-$w)/2 - $w ))
    t='High-intensity colors'
    w=$(echo -n $t | wc -m)
    printf "\033[%dC" $(( (72-$w)/2 ))
    echo $t
    for i in 0 8
    do
	[[ $i != 0 ]] && printf "\033[0m" && printf "\033[30m" ||  printf "\033[1m"
	for j in {0..7}
	do
	    k=$(( $i + $j ))
	    printf "\033[48;5;%dm%9d" $k $k
	done
    done
    printf "\033[0m\n"

    t='216 colors'
    w=$(echo -n $t | wc -m)
    printf "\033[%dC" $(( (144-$w)/2 ))
    echo $t
    for h in {0..5}
    do
	for i in 0 18
	do
	    [[ $i != 0 ]] && printf "\033[0m" && printf "\033[30m" ||  printf "\033[1m"
	    for j in {0..17}
	    do
		k=$(( $i + $j + 36*$h + 16 ))
		printf "\033[48;5;%dm%4d" $k $k
	    done
	done
	printf "\033[0m\n"
    done

    t='Grayscale colors'
    w=$(echo -n $t | wc -m)
    printf "\033[%dC" $(( (144-$w)/2 ))
    echo $t
    for i in 0 12
    do
	[[ $i != 0 ]] && printf "\033[0m" && printf "\033[30m" ||  printf "\033[1m"
	for j in {0..11}
	do
	    k=$(( $i + $j + 232 ))
	    printf "\033[48;5;%dm%6d" $k $k
	done
    done
    printf "\033[0m\n"

    echo
}
colors256
