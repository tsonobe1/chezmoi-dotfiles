# Investigation Flow

原因調査 / 実機確認 mode で読む。

## Steps

1. 再現条件と非再現条件を短く固定する。
2. GUI、権限ダイアログ、log、生成物、永続化ファイルなど、観測点を先に決める。
3. 送信側、受信側、保存、表示、権限、署名、packaging、IPC のように境界を切って事実を集める。
4. current fact と仮説を分けて書く。
5. 原因または修正範囲が確定するまでは `it.todo` / TDD に進まない。
6. keychain、migration dialog、permission prompt などの GUI modal があるときは manual smoke blocker として明示する。
7. CLI で始めた確認でも GUI 承認が入った時点で、自動テストと manual smoke を区別する。
8. manual smoke がユーザ承認や権限待ちで止まるときは、その停止点だけ短く共有する。
9. 同じ runtime failure または manual smoke failure が 2 回以上続くなら、次の retry 前に再現性のある起動導線、1-command smoke、または stable pairing を整える。
10. Electron E2E で EPIPE、crash、stale process、window cleanup failure が出た場合は、feature failure と process/runtime failure を分ける。native rebuild と Electron process cleanup の状態を確認してから再試行する。

## Report Shape

- 再現手順または実機確認手順
- 観測した current facts
- 仮説
- 切り分けた境界
- auto confirmation / runtime blocker / user action needed
- 次の最小アクション
