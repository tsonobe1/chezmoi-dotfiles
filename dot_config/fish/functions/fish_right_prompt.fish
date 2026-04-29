function fish_right_prompt
    set -l cmd_status $status
    if test $cmd_status -ne 0
        echo -n (set_color red)"✘ $cmd_status"
    end

    if not command -sq git
        set_color normal
        return
    end

    if not set -l git_dir (command git rev-parse --git-dir 2>/dev/null)
        set_color normal
        return
    end

    set -l commit ''
    if set -l action (fish_print_git_action "$git_dir")
        set commit (command git rev-parse HEAD 2> /dev/null | string sub -l 7)
    end

    set -l branch_detached 0
    if not set -l branch (command git symbolic-ref --short HEAD 2>/dev/null)
        set branch_detached 1
        set branch (command git describe --contains --all HEAD 2>/dev/null)
    end

    command git rev-list --count --left-right 'HEAD...@{upstream}' 2>/dev/null \
        | read -d \t -l status_ahead status_behind
    if test $status -ne 0
        set status_ahead 0
        set status_behind 0
    end

    set -l status_stashed 0
    if test -f "$git_dir/refs/stash"
        set status_stashed 1
    else if test -r "$git_dir/commondir"
        read -l commondir <"$git_dir/commondir"
        if test -f "$commondir/refs/stash"
            set status_stashed 1
        end
    end

    set -l porcelain_status (command git status --porcelain | string sub -l2)

    set -l status_added 0
    if string match -qr '[ACDMT][ MT]|[ACMT]D' $porcelain_status
        set status_added 1
    end
    set -l status_deleted 0
    if string match -qr '[ ACMRT]D' $porcelain_status
        set status_deleted 1
    end
    set -l status_modified 0
    if string match -qr '[MT]$' $porcelain_status
        set status_modified 1
    end
    set -l status_renamed 0
    if string match -qe R $porcelain_status
        set status_renamed 1
    end
    set -l status_unmerged 0
    if string match -qr 'AA|DD|U' $porcelain_status
        set status_unmerged 1
    end
    set -l status_untracked 0
    if string match -qe '\?\?' $porcelain_status
        set status_untracked 1
    end

    set_color -o

    if test -n "$branch"
        if test $branch_detached -ne 0
            set_color brmagenta
        else
            set_color green
        end
        echo -n " $branch"
    end
    if test -n "$commit"
        echo -n ' '(set_color yellow)"$commit"
    end
    if test -n "$action"
        set_color normal
        echo -n (set_color white)':'(set_color -o brred)"$action"
    end
    if test $status_ahead -ne 0
        echo -n ' '(set_color brmagenta)'⬆'
    end
    if test $status_behind -ne 0
        echo -n ' '(set_color brmagenta)'⬇'
    end
    if test $status_stashed -ne 0
        echo -n ' '(set_color cyan)'✭'
    end
    if test $status_added -ne 0
        echo -n ' '(set_color green)'✚'
    end
    if test $status_deleted -ne 0
        echo -n ' '(set_color red)'✖'
    end
    if test $status_modified -ne 0
        echo -n ' '(set_color blue)'✱'
    end
    if test $status_renamed -ne 0
        echo -n ' '(set_color magenta)'➜'
    end
    if test $status_unmerged -ne 0
        echo -n ' '(set_color yellow)'═'
    end
    if test $status_untracked -ne 0
        echo -n ' '(set_color white)'◼'
    end

    set_color normal
end
