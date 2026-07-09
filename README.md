# chezmoi dotfiles

This repository is the source of truth for local dotfiles managed by `chezmoi`.

## Mac setup

On a new Mac, install `ghq` and `chezmoi`, clone this repository under `ghq`, and initialize `chezmoi` from that source directory.

```bash
brew install ghq chezmoi
ghq get git@github.com:tsonobe1/chezmoi-dotfiles.git
chezmoi init --source "$HOME/ghq/github.com/tsonobe1/chezmoi-dotfiles" --apply
```

これで、chezmoi が管理している `~/.zshrc`、`~/.config/fish/config.fish`、`~/.gitconfig` などが、それぞれ本来の場所に反映されます。

## Source of truth

- Source repo: `~/ghq/github.com/tsonobe1/chezmoi-dotfiles`
- Apply destination: `~`
- Remote: `git@github.com:tsonobe1/chezmoi-dotfiles.git`

`chezmoi` manages the files in this repository and writes them to their real locations such as `~/.gitconfig` and `~/.config/fish/config.fish`.

## Daily workflow

Edit files in this repository first.

Examples:

```bash
cd ~/ghq/github.com/tsonobe1/chezmoi-dotfiles
vi dot_gitconfig
vi dot_config/fish/config.fish
vi private_dot_emacs.d/config/myinit.org
```

Apply changes to the real locations:

```bash
chezmoi apply
```

Check what will change before applying:

```bash
chezmoi diff
```

## Save changes to GitHub

```bash
cd ~/ghq/github.com/tsonobe1/chezmoi-dotfiles
git status
git add .
git commit -m "Update dotfiles"
git push
```

## Managed files

Current examples in this repo:

- `dot_gitconfig` -> `~/.gitconfig`
- `dot_gitignore_global` -> `~/.gitignore_global`
- `dot_tmux.conf` -> `~/.tmux.conf`
- `dot_zprofile` -> `~/.zprofile`
- `dot_zshrc` -> `~/.zshrc`
- `dot_config/fish/config.fish` -> `~/.config/fish/config.fish`
- `dot_config/gh/config.yml` -> `~/.config/gh/config.yml`
- `private_dot_emacs.d/init.el` -> `~/.emacs.d/init.el`
- `private_dot_emacs.d/config/myinit.org` -> `~/.emacs.d/config/myinit.org`
- `run_after_sync-agent-skills.sh.tmpl` -> syncs `~/ghq/github.com/tsonobe1/agent-skills` into Codex and Claude skill directories

## Notes

- Edit the `chezmoi` source files, not the files under `~`, when you want durable changes.
- Run `chezmoi apply` after editing the source files.
- Then commit and push this repository if you want the changes backed up on GitHub.
- Agent skills are managed in `~/ghq/github.com/tsonobe1/agent-skills`, not in this dotfiles repo.
- `~/.codex/skills/.system` and generated/cache-like Codex directories are intentionally not managed here.
