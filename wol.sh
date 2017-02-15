#!/bin/bash

#!/bin/bash

command='/usr/bin/wakeonlan -i 192.168.1.255'
# definition of MAC addresses
fedora=8c:73:6e:73:5b:8c
arch=00:1b:d3:8a:bc:03
# monster=01:12:46:82:ab:4f
# chronic=00:3a:53:21:bc:30
# ghost=01:1a:d2:56:6b:e6

while true; do
echo "Which PC to wake?"
echo "f) fedora"
echo "a) arch"
# echo "c) chronic"
# echo "g) ghost"
# echo "b) wake monster, wait 40sec, then wake chronic"
echo "q) quit and take no action"
read input1

case $input1 in
  f)
  $command $fedora
  ;;

  a)
  $command $arch
  ;;

  # c)
  # /usr/bin/wol $chronic
  # ;;

  # g)
  # # this line requires an IP address in /etc/hosts for ghost
  # # and should use wol over the internet provided that port 9
  # # is forwarded to ghost on ghost's router
  # /usr/bin/wol -v -h -p 9 ghost $ghost
  # ;;

  # b)
  # /usr/bin/wol $monster
  # echo "monster sent, now waiting for 40sec then waking chronic"
  # sleep 40
  # /usr/bin/wol $chronic
  # ;;

  Q|q)
  echo "later!"
  break
  ;;

esac

done
echo  "this is the (quit) end!! c-ya!"
