ZSH=$HOME/.oh-my-zsh
ZSH_THEME="sorin"
plugins=(git)
source $ZSH/oh-my-zsh.sh
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
#source /usr/share/autojump/autojump.sh
PS1="(%{$fg[cyan]%}{{server}}%{$reset_color%}) $PS1"
{% for a,c in aliases.iteritems() %}
alias {{a}}="{{c}}"
{% endfor %}
