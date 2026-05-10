---
name: collab-loop
description: Ugen での実装、レビュー、仕様整理、原因調査を、短い preamble、明示 gate、必要十分な evidence、TDD/品質確認、failure log/ADR判断で進める共同作業ワークフロー。Use when the user says いつもの, 仕様から, todoまで, 承認待ちまで, レビューだけ先に, or asks to follow collab-loop.
---

# Objective

Ugen の共同作業を、次の優先順位で再現可能に進める。

1. 自走力
2. 再現性
3. 学習効率
4. 品質

# Prompt Contract

GPT-5.5 prompt guidance に合わせ、この skill は長い儀式よりも明確な結果、短い control line、必要十分な検証を優先する。

- 最初に user-visible outcome、success criteria、constraints、stop condition を固定する。
- tool-heavy / multi-step 作業では、最初の tool call 前に短い preamble を出す。
- 強い禁止や必須は、承認、安全、検証、破壊的変更、runtime boundary などの hard gate に限定する。
- current file state、repo 契約、公式資料、実測が必要な主張だけを裏取りする。
- 完了前に、変更面に最も関連する validation を選ぶ。実行不能なら blocker と次善の確認を明示する。
- final answer は、`何をしたか`、`ユーザが今できること`、`検証結果`、`未検証点または blocker`、`Next Action` を先に返す。

参考: OpenAI prompt guidance は、複雑な prompt でも各 section を短くし、detail は行動が変わる場合だけ足す方針を推奨している。

# Ugen Doc Lookup Policy

Ugen で仕様監査、実装、レビュー、原因調査をするとき、`docs/fin/*.md` は自動的な初期探索対象にしない。

- current code、current tests、ユーザーが貼った仕様、直近の会話で合意した内容を優先する。
- `docs/fin/*.md` を読むのは、ユーザーが明示したとき、文書更新自体が依頼されたとき、特定ファイル名が提示されたとき、または current code / tests だけでは仕様正本が判断できないときに限る。
- `docs/fin/*.md` を読んだ場合は、なぜ必要だったかを短く説明する。
- `docs/fin/*.md` 内の古い計画・todo・完了メモは current fact として扱わず、必要なら current code / tests / 実測で再確認する。

# Session Preamble

この skill を使う最初の作業メッセージでは、次を短く固定する。

```text
mode: <実装タスク / レビューのみ / 文書更新のみ / repo整理 / 仕様整理のみ / 原因調査>
phase: <spec-audit / todo-drafting / approval-wait / tdd / review / investigation / doc-sync>
stop: <todoまで / 承認待ちまで / commit前まで / findingsで閉じる / skill更新まで>
artifacts: <it.todo, test list, docs, findings, gate result など>
identity: cwd=<path>, worktree=<path>, branch=<name>, spec=<agreed source>, feature=<current feature>
```

`y` / `ｙ` / `ok` を受けたら、次の tool call 前に「この承認で進める単一 action」を 1 文で再掲する。bare approval を review、commit、push など複数 gate にまたがって拡張しない。

# Task Modes

依頼に最も近い mode を先に固定する。

- **実装タスク**: 製品コードやテストの振る舞いを変える。仕様監査、`it.todo`、承認、TDD、品質ゲートを適用する。
- **レビューのみ**: findings first で返して閉じる。実装、`it.todo`、品質ゲートへ進まない。
- **文書更新のみ**: docs、ADR、計画書、skill を更新する。実装用 TDD や `pnpm test` は必須にしない。
- **repo整理 / cleanup**: dead code、不要 script、未採用 spike、内部整理を扱う。user-facing behavior が増えるなら実装タスクへ切り替える。
- **仕様整理のみ**: spec audit と未確定点の整理だけを行う。
- **原因調査 / 実機確認**: 再現、log、GUI観測、runtime boundary の切り分けだけを行う。

詳細な mode 別 artifact は [mode-contract.md](references/mode-contract.md) を読む。

# Stop And Ask

次では止めて確認する。

- 破壊的変更が必要
- 案が拮抗している
- 要件や仕様に矛盾がある
- テスト方針を変える必要がある
- 並列レビューの findings が、承認済み仕様の変更、漏れ、追加 `it.todo` を必要とする
- `it.todo` 提示後にユーザ承認がまだない
- UI/design 参照の visual contract が未承認
- 実測で既存 ADR や設計前提が崩れ、次の実装判断に影響する
- resume、cwd change、worktree change、context transition 後に、現在の cwd / worktree / branch が合意済み正本と一致しない
- 別 worktree / branch から artifact、script、fixture、seed、schema、保存データを持ち込むが、schema / persistence / runtime boundary 互換性が未確認

ユーザが worktree 内のファイル更新を包括許可した場合、通常の編集確認は省略してよい。ただし Stop And Ask の hard gate は残る。破壊的変更、仕様矛盾、テスト方針変更、案の拮抗、legacy migration / storage model 判断、git gate、manual runtime verification は包括許可だけで承認済みにしない。

# Prompt / Skill Tuning Gate

`empirical-prompt-tuning` を使ってこの skill や参照文書を更新する場合は、文書更新のみとして扱う。製品挙動を変えない限り、実装 TDD、`it.todo`、Ugen の `pnpm` gate は n-a にする。

- 編集前に、白紙 subagent による empirical audit を実行し、instruction defect と operation defect を分ける。
- hard gate、必須 artifact、final report 契約、mode 境界を変える patch では、完了前に別の白紙 subagent で hold-out audit を行う。
- audit で出た指摘は current skill text に対する evidence として扱い、指摘をそのまま仕様正本にしない。

# Implementation Flow

実装タスクでは [implementation-flow.md](references/implementation-flow.md) を読む。中核ルールは次。

1. `作業前提`、`今回の製品機能`、`非対象` を分ける。
2. `it.todo` 前に spec audit を行う。
3. 合意済みの全振る舞いを、ユーザーが見る対象・操作・結果で書いた日本語 `it.todo` として提示する。実装名、DOM名、内部型、repository/API名を先に出さない。
4. 既存テストを `残す / 修正する / 不要になる` に棚卸しする。
5. `it.todo` / テストケースが collab-loop の structured test format と user-visible wording contract に準拠しているか、ユーザに聞かれる前に自己点検する。
6. 承認前に Red / Green / Refactor を始めない。
7. 承認後は合意済みの全 `it.todo` を一気通貫で TDD する。
8. TDD 後は並列レビューを行い、findings があれば finding ごとの disposition を残して修正または Stop And Ask へ進む。仕様内修正は再レビューまで自走し、仕様変更や漏れ、明示制約と衝突する finding は勝手に実装しない。
9. runtime boundary、保存、IPC、Quick Launcher、Electron window、theme rehydrate は unit/component test だけで完了扱いしない。

# Review Flow

レビューのみでは [review-flow.md](references/review-flow.md) を読む。中核ルールは次。

- findings first。重大度順に、file / line / 壊れる保証 / current diff から言える根拠を示す。
- 過去 findings が貼られている場合は、各指摘を `resolved` / `still valid` で先に判定する。
- 新しい finding は、過去指摘の判定と混ぜない。
- no findings の場合は明示し、残る test gap / residual risk だけ短く添える。

# UI/design Submode

HTMLモック、スクリーンショット、動画、Figma、「この見た目で」を受けた実装タスクでは、通常の `it.todo` 前に [ui-visual-contract.md](references/ui-visual-contract.md) を読む。

hard gate:

- visual contract 承認前に実装しない。
- layout、state、motion、blur、opacity、hover/selected state を推測で確定しない。
- 実画面確認が必要な UI 変更は、Computer Use、browser-use、スクリーンショット、動画、ユーザ手動確認のどれで証明するかを実装前に決める。
- 実画面証拠がない UI 差分を `resolved` または done 扱いしない。

# Investigation Flow

原因調査 / 実機確認では [investigation-flow.md](references/investigation-flow.md) を読む。中核ルールは次。

- current fact と仮説を分ける。
- 送信、受信、保存、表示、権限、署名、packaging、IPC の境界を切る。
- 原因または修正範囲が確定するまで `it.todo` / TDD に進まない。
- GUI modal、OS permission、manual smoke blocker は自動品質ゲートと分けて報告する。
- 同じ runtime failure が続くなら、retry 前に再現性ある起動導線、1-command smoke、または stable pairing を整える。
- Electron E2E で native module ABI mismatch、native binding load error、EPIPE/crash/stale-window、OS permission denial、または runtime 起動差分が出た場合は、製品修正へ進む前に official E2E gate で再現するか、ABI / process / permission / harness 境界として切り分ける。
- E2E timeout は product bug と即断せず、待っていた対象を特定し、product behavior / selector or test artifact / fixture or saved state / process cleanup / native ABI or tooling のどこで待ちが発生したかを current fact として分類してから修正対象を決める。分類できない場合は product failure と断定しない。

# Quality Gate

mode ごとに最小十分な validation を選ぶ。

- **実装タスク**: 変更面に応じて targeted tests、`pnpm lint`、`pnpm format:check`、`pnpm test`、`pnpm knip`、必要な Electron E2E を選ぶ。
- **Quick Launcher / map mode / editor focus / persistence / theme reflection**: relevant E2E gate を検討する。Quick Launcher から map mode に入る導線を触るなら `pnpm test:e2e:quick-launcher`、同じ flow に theme/style reflection が含まれるなら `pnpm test:e2e:mindmap-style` も対象。
- **Native rebuild を伴う Electron E2E**: `test:e2e:quick-launcher`、`test:e2e:mindmap-style` などが同じ native rebuild / Electron process / generated native artifact に触れる可能性がある場合は serial に実行する。並列実行時の失敗と後続の単独実行 pass が矛盾するときは、最新の単独 official command 結果を current fact、並列時の失敗を runtime/tooling boundary の観測として扱う。
- **文書更新のみ**: 変更ファイル単位の整形、リンク、見出し、参照整合を確認する。
- **レビューのみ / 仕様整理のみ / 原因調査**: 実装用 gate は原則不要。必要なら調査コマンドや再現手順を validation として扱う。

validation result は `targeted gate` と `PR-ready full gate` を分けて報告する。`targeted gate` は変更面に直接対応する最小十分な確認、`PR-ready full gate` は PR 前チェック一式（例: `pnpm lint`、`pnpm format:check`、`pnpm test`、`pnpm build`、`pnpm knip`、relevant E2E）を指す。targeted gate だけが通った場合は `full gate: not-run` と明示し、単に「品質ゲート通過」と書かない。

full gate で追加の drift が見つかった場合は、修正前または最終報告で `feature diff` / `gate-sync diff` / `unrelated diff` に分類する。`gate-sync diff` は今回の feature を PR-ready にするために必要な schema、format、knip、test expectation、E2E harness contract の同期を指し、product behavior の追加変更ではないことを明示する。format / knip / test expectation / E2E harness の差分でも、今回の feature と無関係な既存 drift や別作業差分なら `unrelated diff` に分類する。

validation が走れない場合は `not-run` ではなく、理由と次善の確認を書く。

Native module ABI、rebuild、package install、Electron/Vite process cleanup、OS permission の失敗は、product bug として修正する前に runtime/tooling blocker として分類する。`NODE_MODULE_VERSION`、native binding load error、stale Electron process、permission denial は、それ単体では製品コード修正の根拠にしない。E2E failure が current product behavior と古い harness expectation の不一致だった場合は `harness expectation drift` と分類し、product bug として扱わない。期待値を直す場合は、現仕様の根拠と更新した scenario / helper / assertion を書く。

# Compliance Checkpoint

節目では必要に応じて次を短く出す。長文説明の代わりに gate 状態を見せる。

```text
mode fixed: yes/no
runtime blocker isolated: yes/no/n-a
manual smoke reproducible: yes/no/n-a
spec audit done: yes/no/n-a
it.todo shown: yes/no/n-a
user approval received: yes/no/n-a
implementation started: yes/no
quality gate run: yes/no/n-a
final artifacts ready: yes/no
edit confirmation waived: yes/no/n-a
remaining gates: destructive/spec-conflict/test-policy/competing-approach/git/manual-runtime/n-a
identity verified: yes/no
canonical worktree matched: yes/no/n-a
cross-worktree artifact checked: yes/no/n-a
```

`runtime blocker isolated = yes` は、失敗境界が 1 つに狭まり、根拠となる観測事実を提示できる場合だけ使う。

# Git Gate

commit、push、merge、rebase、review handoff など git gate の前には `git status` を確認し、実行対象の差分や commit 関係がある状態かを短く報告する。

- `y` / `ok` の継続承認を commit 承認として扱わない。commit 承認後も、実行直前に commit 可能性を再確認する。
- 依頼内容が未追跡 artifact の削除だけなら、それは commit 対象にならない。削除後に worktree が clean なら、新しい commit は作れないと commit 前に伝える。
- merge / rebase / branch integration では、実行直前に target branch との commit 関係と worktree 状態を確認する。すでに同一 commit、up-to-date、または push 対象なしなら実行前に止める。
- git 結果がユーザー期待とズレる場合は、commit / push 前に止めて「作る commit がない」「対象差分は既存 commit 済み」などを明示する。
- commit 前に staged / unstaged の差分を `feature diff` / `gate-sync diff` / `unrelated diff` に分類し、今回 commit に含めるものと分けるものを報告する。`gate-sync diff` を feature commit に含める場合は、今回の変更を PR-ready にするための同期であることを明示する。`unrelated diff` は原則として含めない。
- `unrelated diff` が残っているため full gate が PR-ready と言えない場合は、今回 commit から除外し、final で `full=<fail or not-ready>` と残課題を明示する。
- final report では `commit: created <hash>` / `commit: not-created clean worktree` / `commit: already-existing <hash or unknown>` と、git action 全般の `action: not-needed` / `action: already-existing` を区別して書く。

# Parallel Work

別 agent を使う場合だけ、役割分担を明示する。

- Spec agent: spec audit と未確定点抽出
- Implementation agent: 承認済み `it.todo` の実装
- Review agent: current diff / current file contents から findings first review
- Audit agent: hard gate と artifact の欠落確認

別 agent を実際に起動していないなら、独立 review / audit が完了したと報告しない。単独 agent の自己点検は `not independent` と明示する。

実装タスクでは、TDD 完了後の review gate に原則として複数の Review/Audit agent を使う。findings が出た場合は、各 finding を `fixed` / `needs user confirmation` / `rejected by current constraint` / `not reproduced` / `deferred` のいずれかに disposition してから review gate 完了を主張する。承認済み仕様の範囲内なら修正、必要な validation、再度の並列レビューまで継続する。ユーザ確認が必要なのは、finding が仕様変更、未承認の追加仕様、テスト方針変更、破壊的変更、または案の拮抗を含む場合だけ。finding が明示済み制約（例: fallback 不要、migration 不要、後方互換不要）と衝突する場合は、0 findings にするために実装せず、evidence 付きで `rejected by current constraint` または Stop And Ask にする。

# Failure Log And ADR

完了前に必ず次を明示する。

```text
failure log: recorded / not-needed
ADR: recorded / not-needed
```

- failure log は、再発しうる失敗や認識ズレがあったとき `/Users/tsonobe/.codex/memories/collab_failure_log.md` に残す。
- ADR は、今後の実装判断に繰り返し影響する設計方針を採用または撤回したときに残す。
- 局所的な文書更新や prompt 整理だけなら `not-needed` とし、理由を一文で添える。

# Final Report

最終報告は outcome-first にする。

1. 何をしたか
2. ユーザが今できること
3. 検証結果
4. 未検証点または blocker
5. 判断理由
6. Next Action
7. failure log / ADR
8. 実装タスクの場合だけ Collab Audit

実装タスクの Collab Audit は [collab-audit-template.md](references/collab-audit-template.md) を使う。レビューのみ、文書更新のみ、仕様整理のみ、原因調査では必須にしない。

実装タスクで Review-Fix loop を回した後の最終報告では、`ユーザが今できること` を必ず具体的な操作・表示・制約で説明する。内部変更やテスト通過だけで終わらせず、「ユーザー目線で何が増えたか / 何が安全になったか / まだ何ができないか」を短く書く。

Review-Fix loop を回した場合は、finding disposition と residual risk を短く書く。未承認の仕様変更、legacy migration、破壊的変更、テスト方針変更を `approved` / `合意済み` と書かない。包括編集許可で進めた範囲と、未解決 gate を分けて書く。

実装タスクの final は、短くても次の footer を落とさない。commit 後の final でも、commit 結果だけに縮退させず実装 final artifact を残す。

```text
quality gate: targeted=<pass/fail/not-run>, full=<pass/fail/not-run>, e2e=<pass/fail/not-run/n-a>
scope: feature diff=<included/n-a>, gate-sync diff=<included/separate/n-a>, unrelated diff=<excluded/n-a>
failure log: recorded / not-needed
ADR: recorded / not-needed
Collab Audit: included / n-a
commit: created <hash> / not-created <reason> / n-a
```

hard gate や mode 契約を破った場合は `protocol violation` を明示し、何を破ったか、いつ破ったか、信頼性への影響、次回の防止策を書く。違反がなければ必要に応じて `protocol violation: none` と短く書く。

# Invocation

次を起動句として扱う。

- `$collab-loop に従って進める`
- `いつもの`
- `いつもの流れで`
- `仕様から`
- `todoまで`
- `承認待ちまで`
- `レビューだけ先に`
- `修正をいつもの流れで`
- `機能追加をいつもの流れで`

短い例は [request-templates.md](references/request-templates.md) を読む。

Ugen では、この skill を共同作業の主契約として扱う。`workflow` や `ugen-development` と重なる内容がある場合、この skill の hard gate と進行手順を優先する。
