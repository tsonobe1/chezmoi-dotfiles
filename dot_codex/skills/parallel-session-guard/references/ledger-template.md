# Parallel Session Ledger

更新時刻: `YYYY-MM-DD HH:MM TZ`

| status | session_id | worktree | branch | scope | reserved_paths | note |
| --- | --- | --- | --- | --- | --- | --- |
| active | 019dxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | /abs/path/to/worktree | codex/example-task | mindmap bugfix | src/features/mindmap/editor, src/features/tests/mindmap/editor | avoid ViewPort.vue overlap |

## Status Values

- `planned`
- `active`
- `blocked`
- `done`
- `abandoned`

## Update Rules

- 新しい並列作業を始める前に 1 行追加する
- `scope` はユーザ価値か feature 名で書く
- `reserved_paths` は file でも directory でもよいが、曖昧な `mindmap 全部` は避ける
- 作業終了時に `status` を更新する
- ユーザが求めない限り、この ledger は commit しない
