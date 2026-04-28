# chezmoi dotfiles

This repository is the source of truth for local dotfiles managed by `chezmoi`.

## Source of truth

- Source repo: `~/.local/share/chezmoi`
- Apply destination: `~`
- Remote: `git@github.com:tsonobe1/chezmoi-dotfiles.git`

`chezmoi` manages the files in this repository and writes them to their real locations such as `~/.gitconfig` and `~/.config/fish/config.fish`.

## Daily workflow

Edit files in this repository first.

Examples:

```bash
cd ~/.local/share/chezmoi
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
cd ~/.local/share/chezmoi
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
- `private_dot_emacs.d/config/myinit.org` -> `~/.emacs.d/config/myinit.org`

## Notes

- Edit the `chezmoi` source files, not the files under `~`, when you want durable changes.
- Run `chezmoi apply` after editing the source files.
- Then commit and push this repository if you want the changes backed up on GitHub.
