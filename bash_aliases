# # enable color support of ls and also add handy aliases
# if [ -x /usr/bin/dircolors ]; then
#     test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
#     alias ls='ls --color=always -F'
#     #alias dir='dir --color=auto'
#     #alias vdir='vdir --color=auto'
# fi
# # some more ls aliases
# alias ll='ls -alF'
# alias la='ls -A'
# alias l='ls -CF'
# # Add an "alert" alias for long running commands.  Use like so:
# #   sleep 10; alert
# alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

alias ls="ls -F --color=always"
alias grep='grep --color=always'
alias fgrep='fgrep --color=always'
alias egrep='egrep --color=always'

alias less="less -R"
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"
alias em="emacs -nw"
