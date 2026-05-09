# Mode Contract

各 mode の artifact と完了条件をここに集約する。`SKILL.md` には中核だけ置き、迷ったときだけこの reference を読む。

## 実装タスク

必要 artifact:

- Session Preamble
- Compliance Checkpoint
- worktree identity result（cwd / worktree / branch / spec 正本 / test inventory / current feature）
- 作業前提 / 今回の製品機能 / 非対象
- spec audit 結果
- 合意済みの全振る舞いを並べた `it.todo`
- 構造化テスト一覧
- 既存テストへの影響棚卸し（`残す / 修正する / 不要になる`）
- validation 結果
- `failure log: recorded/not-needed`
- `ADR: recorded/not-needed`
- Collab Audit

完了条件:

- ユーザ承認後に合意済みの全 `it.todo` が Red / Green / Refactor を通っている
- 変更面に最も関連する validation を実行済み、または blocker と次善確認を明示済み
- runtime boundary や manual smoke が関係する場合、`auto gates`、`runtime smoke`、`done status` を分けている

## レビューのみ

必要 artifact:

- Session Preamble
- Compliance Checkpoint
- findings first の結果
- open questions / assumptions（必要な場合）
- Next Action

完了条件:

- 実装や docs 更新へ勝手に進んでいない
- 過去 findings が貼られている場合は `resolved` / `still valid` を先に返している

## 文書更新のみ

必要 artifact:

- Session Preamble
- Compliance Checkpoint
- 変更した文書一覧
- empirical pre-edit audit result（`empirical-prompt-tuning` invoked 時）
- hold-out audit result（hard gate / artifact contract / mode boundary を変えた時）
- 変更ファイル単位の確認結果
- `failure log: recorded/not-needed`
- `ADR: recorded/not-needed`
- Next Action

完了条件:

- docs / ADR / skill / 計画書だけを更新している
- 実装用 gate を不要にする理由が明示されている

## repo整理 / cleanup

必要 artifact:

- Session Preamble
- Compliance Checkpoint
- current mainline / 非採用 spike の判定
- cleanup 対象一覧
- 既存テストへの影響棚卸し
- 変更ファイル単位の確認結果
- `failure log: recorded/not-needed`
- `ADR: recorded/not-needed`

完了条件:

- user-facing behavior を増やしていない
- feature-style `it.todo` や新規 user-facing test を不要にした理由が説明できる

## 仕様整理のみ

必要 artifact:

- Session Preamble
- Compliance Checkpoint
- spec audit 結果
- 未確定点または合意済み next step
- Next Action

完了条件:

- 実装や品質ゲートへ勝手に進んでいない

## 原因調査 / 実機確認

必要 artifact:

- Session Preamble
- Compliance Checkpoint
- 再現手順または実機確認手順
- 観測した事実と証拠
- 切り分けた境界または次の仮説
- `failure log: recorded/not-needed`
- `ADR: recorded/not-needed`
- Next Action

完了条件:

- current fact と仮説を分けている
- 自動テスト、runtime failure、GUI blocker、user action needed を混ぜていない
