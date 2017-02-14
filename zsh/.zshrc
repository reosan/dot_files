autoload -U compinit promptinit
compinit
promptinit

# This will set the default prompt to the walters theme
prompt walters

autoload -Uz colors
colors

RSTACKFILE="$HOME/.cache/zsh/dirs"
if [[ -f $DIRSTACKFILE ]] && [[ $#dirstack -eq 0 ]]; then
  dirstack=( ${(f)"$(< $DIRSTACKFILE)"} )
	  [[ -d $dirstack[1] ]] && cd $dirstack[1]
		fi
		chpwd() {
		  print -l $PWD ${(u)dirstack} >$DIRSTACKFILE
			}

			DIRSTACKSIZE=20

			setopt autopushd pushdsilent pushdtohome

			## Remove duplicate entries
			setopt pushdignoredups

			## This reverts the +/- operators.
			setopt pushdminus


			autoload -U run-help
			autoload run-help-git
			autoload run-help-svn
			autoload run-help-svk
			unalias run-help
			alias help=run-help




# PROMPT='%{$fg[red]%}[%n@%m]%{$reset_color%}'
# RPROMPT='%{${fg[red]}%}[%~]%{${reset_color}%}'

# create a zkbd compatible hash;
# to add other keys to this hash, see: man 5 terminfo
typeset -A key

key[Home]=${terminfo[khome]}

key[End]=${terminfo[kend]}
key[Insert]=${terminfo[kich1]}
key[Delete]=${terminfo[kdch1]}
key[Up]=${terminfo[kcuu1]}
key[Down]=${terminfo[kcud1]}
key[Left]=${terminfo[kcub1]}
key[Right]=${terminfo[kcuf1]}
key[PageUp]=${terminfo[kpp]}
key[PageDown]=${terminfo[knp]}

# setup key accordingly
[[ -n "${key[Home]}"     ]]  && bindkey  "${key[Home]}"     beginning-of-line
[[ -n "${key[End]}"      ]]  && bindkey  "${key[End]}"      end-of-line
[[ -n "${key[Insert]}"   ]]  && bindkey  "${key[Insert]}"   overwrite-mode
[[ -n "${key[Delete]}"   ]]  && bindkey  "${key[Delete]}"   delete-char
[[ -n "${key[Up]}"       ]]  && bindkey  "${key[Up]}"       up-line-or-history
[[ -n "${key[Down]}"     ]]  && bindkey  "${key[Down]}"     down-line-or-history
[[ -n "${key[Left]}"     ]]  && bindkey  "${key[Left]}"     backward-char
[[ -n "${key[Right]}"    ]]  && bindkey  "${key[Right]}"    forward-char
[[ -n "${key[PageUp]}"   ]]  && bindkey  "${key[PageUp]}"   beginning-of-buffer-or-history
[[ -n "${key[PageDown]}" ]]  && bindkey  "${key[PageDown]}" end-of-buffer-or-history

# Finally, make sure the terminal is in application mode, when zle is
# active. Only then are the values from $terminfo valid.
if (( ${+terminfo[smkx]} )) && (( ${+terminfo[rmkx]} )); then
    function zle-line-init () {
		        printf '%s' "${terminfo[smkx]}"
						    }
								    function zle-line-finish () {
										        printf '%s' "${terminfo[rmkx]}"
														    }
																    zle -N zle-line-init
																		    zle -N zle-line-finish
																				fi
