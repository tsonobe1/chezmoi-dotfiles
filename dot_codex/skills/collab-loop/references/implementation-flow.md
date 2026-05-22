# Implementation Flow

実装タスクで読む。作業前提を製品機能に混ぜず、合意済みの振る舞いだけを TDD 対象にする。

## Scope Boundary

`it.todo` は今回ユーザが求めた製品機能またはユーザーに見える振る舞いだけを書く。

作業を進めるために必要な merge、rebase、conflict 解消、branch 取り込み、依存差分の同期、既存未コミット差分の退避、format は `作業前提` として扱い、製品機能の `it.todo` に混ぜない。

`it.todo` を提示する前に必ず分ける。

- `作業前提`: merge、branch 取り込み、conflict 解消、既存差分の保護など
- `今回の製品機能`: ユーザが今回実装したい振る舞い
- `非対象`: 今回は実装しない振る舞い、未確定仕様、別 branch / 別 feature の作業

スコープ誤りに気づいたら、実装へ進まず `scope-correction` としてやり直す。

## Worktree Identity Boundary

実装前、resume 後、cwd change 後、worktree change 後、context transition 後は、合意済み正本を current fact として確認する。

- `cwd`、worktree path、branch、spec 正本、test inventory、current feature を出す。
- 現在地が合意済み正本と違う場合は実装へ進まず、正本へ戻るか、差分棚卸しへ切り替える。
- 誤った worktree に差分がある場合は、まず `unrelated` / `accidental` / `salvageable` に分類し、feature worktree へ持ち込む前にユーザ確認する。
- 別 worktree / branch の artifact、script、fixture、seed、schema、保存データを使う場合は、schema / persistence / runtime boundary の互換性を確認する。不一致または未確認なら Stop And Ask に戻す。

## Spec Audit Before `it.todo`

最低限、次を確認する。

- 対象の振る舞いと非対象の範囲が明確か
- 前提条件、事後条件、不変条件が揃っているか
- 正常系、異常系、境界条件に漏れがないか
- テスト観点に落とせない曖昧な文言が残っていないか
- テストが製品仕様を保証しており、ランナーや fixture 都合を保証対象に混ぜていないか
- UI/design 参照がある場合、visual contract と evidence plan があるか
- Electron IPC、structuredClone、preload/main、renderer/main、永続化 storage、外部プロセスなどの runtime boundary があるか
- runtime boundary を通る値が plain data として仕様化されているか
- 保存や IPC がある場合、保存 state shape、再読込後の復元、境界通過後 payload を evidence plan に含めているか
- 文書タスクや ADR 更新では、既存の repo 配置と命名規則を確認しているか
- アプリケーションアーキテクチャの各レイヤで、どの spec ファイルに `it.todo` を置くべきか判断できるか
- 既存テストを `残す / 修正する / 削除する / 不要になる` に棚卸しできるか
- 更新または削除すべき既存テストケースを説明できるか
- 不要になるテストは、どの仕様から外れたか説明できるか

曖昧さが残る場合は、`it.todo` を書く前に確認する。

## Structured Test Format

`it.todo` とテストケース一覧は、次の構造で提示する。

- 作業前提
- 今回の製品機能
- 非対象
- 対象機能
- 観点カテゴリ
- 個別振る舞い
- spec ファイルごとの `it.todo`
- 既存テストへの影響

観点カテゴリ:

- 正常系
- 異常系
- 境界条件
- 前提条件
- 契約・不変条件
- Runtime boundary
- Persistence / rehydrate

各 `it.todo` は日本語で、条件 + 結果の形式にする。メソッド名の言い換えや実装詳細ではなく、製品の振る舞いを書く。

`it.todo` はアプリケーションアーキテクチャの各レイヤに置くことを想定し、各 spec ファイルごとに作成する。ドメイン、アプリケーションサービス / composable、UI component、IPC / persistence、E2E など、どのレイヤの spec でどの振る舞いを保証するかを分ける。該当しないレイヤは `n-a` とし、存在しない spec ファイルを無理に増やさない。

## User-visible `it.todo` Wording Contract

`it.todo` は、先にユーザーの画面・操作・結果として書き、必要な技術語は後続の evidence plan や実装メモへ逃がす。

書く順序:

1. ユーザーが見る対象: 例 `削除済み参照`、`通常の外部参照`、`履歴バー`
2. ユーザー操作または状態: 例 `クリックしたとき`、`複数あるとき`、`開き直したとき`
3. ユーザーに見える結果: 例 `移動できる`、`参照リンクだけ削除できる`、`同じ位置に戻る`

避ける語:

- DOM / test id 語: `ghost`、`data-test`、`DOM`、`selector`
- 内部型 / 状態語: `valid target link`、`invalid target link`、`source node`、`operationId`
- repository / API 語: `repository 正本`、`IPC`、`payload`、`method`
- 実装手段語: `emit する`、`ref を更新する`、`computed に含まれる`

置き換え例:

- NG: `valid target link と invalid target link が混在するとき valid link は移動でき invalid link は削除だけできる`
- OK: `同じノードに通常の外部参照と削除済み参照が混在するとき、通常の参照は移動でき、削除済み参照は参照リンクだけ削除できる`
- NG: `複数の invalid target link が同じ source node にあるとき件数と ghost 数が一致する`
- OK: `同じノードに削除済み参照が複数あるとき、外部リンクの件数表示と表示される削除済み参照の数が一致する`
- NG: `invalid target link delete の undo / redo 後に source 側表示が repository 正本と一致する`
- OK: `削除済み参照の削除を undo または redo したあと、画面表示が保存済みの参照リンク状態と一致する`

自己点検:

- テスト名だけを読んで、ユーザーが何をできるようになるか分かるか。
- 実装ファイル名、関数名、型名、DOM名を知らない人にも伝わるか。
- 技術語が必要な場合、それは `it.todo` ではなく evidence plan / test implementation に置けないか。
- 「内部的に何を呼ぶか」ではなく「ユーザーから見て何が起きるか」を検証しているか。

テストケースを提案または実装する前に、ユーザに「collab-loop に準拠しているか」と聞かれなくても自己点検する。最低限、`作業前提 / 今回の製品機能 / 非対象 / 対象機能 / 観点カテゴリ / 個別振る舞い / spec ファイルごとの it.todo / 既存テストへの影響` が埋まっているか、各 `it.todo` が条件 + 結果になっているか、user-visible wording contract に反していないか、runtime boundary の evidence plan があるかを確認する。不足があれば実装前に補う。

既存テストへの影響:

- `残す`: 現仕様でもそのまま保証対象
- `修正する`: 仕様確定に合わせて名前、前提、期待値、責務境界を更新
- `削除する`: 現仕様では誤った保証、重複、または廃止済み責務を固定しており、削除対象
- `不要になる`: 今回の仕様確定で保証対象から外れる、または比較元の誤りが判明

## TDD Policy

- 汎用的なテストケース設計原則は `../../tdd/test-case-principles.md` に従う。ここでは Ugen 固有の workflow、承認、配置、runtime boundary、quality gate を追加する。
- classical school を採用する
- t-wada style TDD に従う
- テスト名は日本語で、条件 + 結果を表現する
- 承認済みの全 `it.todo` を対象に完了まで進める
- 実装途中で新しい振る舞いが必要になったら、勝手に足さず仕様更新の確認へ戻る
- 包括的なファイル更新許可がある場合も、ユーザ確認なしで進めてよいのは承認済み仕様内の編集だけにする

## Review-Fix Loop After TDD

承認済み `it.todo` の Red / Green / Refactor が終わったら、完了報告や commit へ進む前に review gate へ進む。

1. current diff / current file contents を対象に、複数の Review/Audit agent で並列レビューする。
   Review/Audit agent は product runtime behavior だけでなく、docs・test名・E2E scenario名・helper API・TypeScript型・harness contract の drift も current diff から確認する。
2. findings がない場合は、validation と残リスクをまとめて commit 前 gate へ進む。
3. findings がある場合は、各 finding を `仕様内修正` / `仕様変更または漏れ` / `テスト方針変更` / `破壊的変更` / `判断保留` に分類する。
4. `仕様内修正` はユーザ確認を待たず、TDD の続きとして修正する。必要なら regression test を先に追加し、Green / Refactor / relevant validation を行う。
5. 各 finding は最終的に `fixed` / `needs user confirmation` / `rejected by current constraint` / `not reproduced` / `deferred` のいずれかに disposition し、根拠を残す。
6. finding が明示済み制約（例: fallback 不要、migration 不要、後方互換不要）と衝突する場合は、0 findings にするために実装しない。制約自体を見直す必要があるなら Stop And Ask、見直し不要なら `rejected by current constraint` にする。
7. subagent の validation 失敗は、親 session の official gate 結果と分けて扱う。native ABI、process cleanup、permission、harness 差分が疑われる失敗は、official gate で再現するまで product finding と断定しない。
8. gate-sync diff は、今回の feature を PR-ready にするために必要な schema、format、knip、test expectation、E2E harness contract の同期を指す。product behavior の追加変更ではないことを finding disposition に残す。
9. E2E failure が current product behavior と古い harness expectation の不一致だった場合は `harness expectation drift` と分類し、product bug として扱わない。期待値を直す場合は、現仕様の根拠と更新した scenario / helper / assertion を書く。
10. 修正後は再び複数の Review/Audit agent で並列レビューする。
11. `fixed` できる findings が 0 になり、残った finding の disposition と residual risk が説明できるまで 3-10 を繰り返す。
12. `仕様変更または漏れ`、`テスト方針変更`、`破壊的変更`、`判断保留` は Stop And Ask に戻し、ユーザ承認なしに実装しない。

この loop は commit 承認や push 承認を含まない。review gate が完了しても、git gate は別に扱う。

## Implementation Rules

- 最小実装でテストを通す
- 不要な fallback を入れない
- 後方互換のためだけの分岐を入れない
- 関心の分離を保つ
- 状態とロジックを分離する
- 実装とテストの契約が一致しているか確認する
- 静的検査可能なルールは prompt ではなく linter / type / test に寄せる
