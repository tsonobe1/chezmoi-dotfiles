# chezmoi dotfiles

シェル・Git・tmux・Emacs など、PC の設定ファイルを管理するリポジトリです。
このリポジトリを編集し、`chezmoi apply` で実際の使用場所へ反映します。
スキル本体の編集・変更履歴は [agent-skills](https://github.com/tsonobe1/agent-skills) が担当します。

## 責務と使い分け

| やりたいこと | 編集先・使うもの |
| --- | --- |
| シェル・Git・tmux・Emacs などの設定を変える | このリポジトリの対応ファイル |
| Codex が作業全般で守るルールを変える | `dot_codex/AGENTS.md` |
| 設定を PC に反映する | `chezmoi diff` → `chezmoi apply` |
| 設定の変更を GitHub に保存する | このリポジトリで commit / push |
| スキルの内容を変える、追加・削除する | `agent-skills`。操作はそちらの README を参照 |
| 新しい PC に環境を用意する | 下記の Mac セットアップ。スキル環境の準備処理も含む |

管理元は `~/ghq/github.com/tsonobe1/chezmoi-dotfiles`、反映先はホームディレクトリです。
ghq はリポジトリの取得・配置を整理し、chezmoi は設定を使用場所へ反映します。
この構成では、設定は通常のファイルとして配置します。

## 普段の設定変更

1. このリポジトリの対象ファイルを編集する。
2. `chezmoi diff` で使用中のファイルとの差分を確認する。
3. `chezmoi apply` で、管理元の内容を使用場所へ反映する。
4. 変更したファイルを選んで commit / push する。

例えば Zsh の設定を変更する場合:

```bash
cd "$HOME/ghq/github.com/tsonobe1/chezmoi-dotfiles"
vi dot_zshrc
chezmoi diff
chezmoi apply
git diff
git add -- dot_zshrc
git commit -m "Keep shell setup reproducible across Macs"
git push
```

使用場所のファイルを直接編集した場合は、`chezmoi diff` で比較し、採用する変更を
`chezmoi add` で管理元へ取り込みます。例えば `chezmoi add "$HOME/.zshrc"` です。
`apply` は管理元から使用場所への反映なので、使用場所の変更を残したいときは先に確認します。

## 管理している設定

| 設定 | 管理元 → 使用場所 |
| --- | --- |
| Git | `dot_gitconfig` → `~/.gitconfig`、`dot_gitignore_global` → `~/.gitignore_global` |
| Zsh | `dot_zprofile` → `~/.zprofile`、`dot_zshrc` → `~/.zshrc` |
| Fish | `dot_config/fish/` の起動設定・プロンプトなど → `~/.config/fish/` の対応ファイル |
| GitHub CLI | `dot_config/gh/config.yml` → `~/.config/gh/config.yml` |
| tmux | `dot_tmux.conf` → `~/.tmux.conf` |
| Emacs | `private_dot_emacs.d/init.el` と `private_dot_emacs.d/config/myinit.org` → `~/.emacs.d/` の対応ファイル |
| Codex の作業ルール | `dot_codex/AGENTS.md` → `~/.codex/AGENTS.md` |
| chezmoi | `dot_config/chezmoi/chezmoi.toml.tmpl` → `~/.config/chezmoi/chezmoi.toml` |

説明用のこの README も `~/README.md` に配置します。
管理対象の正確な一覧は `chezmoi managed --include=files,symlinks` で確認できます。
Codex の標準スキル・プラグイン・会話履歴などは、このリポジトリの管理対象に含まれません。

## Codex の AGENTS.md とスキルの違い

どちらも指示を書くファイルですが、使う場面が異なります。

| 種類 | 役割・例 | 管理するリポジトリ |
| --- | --- | --- |
| `~/.codex/AGENTS.md` | 作業全般に適用するルール。現在は作業報告の書き方や、別セッションへの依頼方法 | このリポジトリの [dot_codex/AGENTS.md](./dot_codex/AGENTS.md) |
| スキルの `SKILL.md` | 必要に応じて読み込む、特定の作業の手順。例えば TDD、レビュー、UI 仕様の策定 | [agent-skills](https://github.com/tsonobe1/agent-skills) |

## agent-skills との連携

[準備処理](./run_onchange_after_sync-agent-skills.sh.tmpl) は、初回、または処理自体の内容が
変わったときに、`chezmoi apply` の中で次を行います。

1. `agent-skills` がなければ、`~/ghq/github.com/tsonobe1/agent-skills` に clone する。
2. そのリポジトリの `scripts/sync-live.sh` を呼び、Codex / Claude / Grok Build 側のリンクを整える。

既存の `agent-skills` に対する pull や、スキルの内容の編集は、この準備処理には含まれません。
日常のスキル編集は `agent-skills` で行い、各ツールはリンク先の本体を読みます。
新しいスキルのリンク作成、変更の commit / push も、`agent-skills` 側の運用です。

## 新しい Mac のセットアップ

GitHub のリポジトリを取得できる状態で、ghq と chezmoi を導入し、設定を反映します。

```bash
brew install ghq chezmoi
ghq get git@github.com:tsonobe1/chezmoi-dotfiles.git
chezmoi init --source "$HOME/ghq/github.com/tsonobe1/chezmoi-dotfiles" --apply
```

スキルの commit 後・merge 後にリンクを自動整備する Git hook は、別途一度だけ設定します。

```bash
"$HOME/ghq/github.com/tsonobe1/agent-skills/scripts/install-hooks.sh"
```

以降のスキル編集・同期は、[agent-skills の README](https://github.com/tsonobe1/agent-skills) を参照します。
