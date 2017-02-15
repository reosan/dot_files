#!/bin/sh

sub=1
[ $# -eq 1 ] && sub=$1

echo ping 192.168.$sub.1-254...
for i in `seq 1 254`
do
	echo "$i/254"; printf "\033[A"
	ping -c 1 -w 0.5 192.168.$sub.$i > /dev/null \
		&& arp -a 192.168.$sub.$i | grep ether
done

