# UI/design Submode

HTMLモック、スクリーンショット、動画、Figma、または「この見た目で」という UI/design 参照を受け取った実装タスクで読む。

## Phases

- `visual-intake`
- `visual-contract`
- `approval-wait`
- `implementation`
- `visual-review`

UI/design submode は独立した task mode ではない。通常は `実装タスク` の前段として使う。比較や差分整理だけなら `仕様整理のみ` または `原因調査 / 実機確認` に留める。

## Required Artifacts

- 参照資料一覧
- visual contract
- 未確定点
- evidence plan
- approval-wait の明示

## Visual Contract Template

| Area | Reference | Must match | Approximate ok | Unknown / needs decision |
| --- | --- | --- | --- | --- |
| Search UI |  |  |  |  |
| Result list |  |  |  |  |
| Preview |  |  |  |  |
| Map mode |  |  |  |  |
| Motion / transition |  |  |  |  |
| Blur / opacity / background |  |  |  |  |

Quick Launcher、Electron window、IPC、保存、再読込をまたぐ UI 変更では、visual contract に preview、mode switch、keyboard focus、persistence、rehydrate、theme/style reflection を別 Area として含める。

動画を受け取ったときは、必要に応じて代表フレームを求める。最低限、`入力前`、`入力中または結果表示中`、`preview 表示時`、`mode 切替直後` のどれが正かを固定する。

## Visual Review

実装後または「見た目が違う」と指摘された後は、差分を必ず 4 分類で返す。

- `resolved`: 実画面証拠で参照と一致した
- `remaining`: 差分が残っている
- `intentional`: 参照と違うが、理由と承認がある
- `unverified`: 実画面証拠がなく完了扱いできない

該当項目がない場合も `intentional: none` のように明示する。
