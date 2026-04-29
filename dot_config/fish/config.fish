if status is-interactive
    # Commands to run in interactive sessions can go here
end

# homebrew path
set PATH /opt/homebrew/bin/  $PATH

# nodebrew path
set -x PATH $HOME/.nodebrew/current/bin:$PATH


# ----------- alias ---------------
alias tm='tmux'
alias vi='nvim'
alias g='git'

# ビジネス用 Git 設定
function gbiz
    git config --global user.name "sonobe-takuto"
    git config --global user.email "sonobe.takuto@sunborn.co.jp"
    git config user.name
    git config user.email
end

# プライベート用 Git 設定
function gpri
    git config --global user.name "tsonobe1"
    git config --global user.email "sono.tak.st@gmail.com"
    git config user.name
    git config user.email
end

# Git エイリアス
alias g='git'

alias gs='git status'
alias glo='git log'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'
alias ga='git add'
alias gai='git add -i'
alias gcl='git clone'
alias gpl='git pull'

# インタラクティブな Git ブランチ切り替え
function gcoi
    git branch -a | fzf | while read -l line
        git switch (string trim -- $line)
    end
end

# ls command color change => chien
export LSCOLORS=gxfxcxdxbxegedabagacad
set -g fish_color_match --background=brblue

# pnpm
set -gx PNPM_HOME "/Users/tsonobe/Library/pnpm"
if not string match -q -- $PNPM_HOME $PATH
  set -gx PATH "$PNPM_HOME" $PATH
end
# pnpm end

# ghq / fzf / zoxide
if type -q zoxide
    zoxide init fish | source
end

function cghq --description "Select a ghq-managed repository and cd there"
    if not type -q ghq
        echo "ghq is not installed" >&2
        return 1
    end

    if not type -q fzf
        echo "fzf is not installed" >&2
        return 1
    end

    set -l selected (ghq list --full-path | fzf --height 40% --reverse)
    if test -n "$selected"
        cd -- "$selected"
    end
end

# Added by Antigravity
fish_add_path /Users/tsonobe/.antigravity/antigravity/bin
