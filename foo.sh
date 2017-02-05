#!/bin/bash
colors256() {
  local i j k
  printf "\n"
  for i in {0..27}
  do
      printf " "
  done
  printf "\033[1m\\\033[38;5;\033[4m%%d\033[0;1mm"
  printf "\033[G"
  printf "\033[%dC" $((3+16*4+2))
  for i in {0..27}
  do
      printf " "
  done
  printf "\\\033[48;5;\033[4m%%d\033[0;1mm\n\n\033[0m"
  
  printf "   "
  for i in {0..15}
  do
    printf " %X  " $i      
  done
  printf "     "
  for i in {0..15}
  do
    printf " %X  " $i      
  done
  printf "\n"

  for i in {0..15}
  do
      printf " %X " $i

      for j in {0..15}
      do
	  k=$(($i*16+$j))
	  printf "\033[38;5;%dm%03d " $k $k
      done
      printf "  "

      printf " \033[0m%X " $i
      for j in {0..15}
      do
	  k=$(($i*16+$j))
	  printf "\033[48;5;%dm%03d" $k $k
	  printf "\033[0m "
      done
      printf "\n\n"

  done
  
  printf "\033[0m "
}
colors256
