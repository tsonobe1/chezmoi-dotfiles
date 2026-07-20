---
name: parallel-session-guard
description: Use when work may overlap another Codex session, branch, worktree, or changed file; when active session ownership must be checked; or when follow-up work may need to be queued to an existing owning session.
---

# Objective

複数の Codex セッションを同時に進める前に、最近の作業と現在の Git 状態を照合し、競合しにくい作業領域を決める。

**Core principle:** 同じbranch、編集領域、または設計責任の所有者を増やさない。ファイルの重複だけでは競合と断定せず、変更するsymbol・責務・仕様を比較する。所有セッションが実行中なら、そのturnを中断せず、ユーザーへ説明してから後続キューへ積む。

# Use This Skill For

- `並列で進めたい`
- `今アクティブな session を確認して`
- `main で何をやっているか確認して`
- `このタスクが既存作業とぶつからないか見て`
- `安全な worktree / branch を切って`
- `担当ファイルを予約したい`

# Outputs

- recent session inventory
- worktree / branch inventory
- overlap assessment
- recommendation:
  - existing worktree を再利用する
  - 新しい worktree を切る
  - clean な worktree に新しい branch を切る
  - owning session の後続キューへ積む
  - 競合が強いので確認待ちにする
- 必要なら reservation ledger の更新

# Workflow

1. 現在の repo root、worktree、branch を確認する。
2. 直近の Codex session を集める。
   - `python3 /Users/tsonobe/.codex/skills/parallel-session-guard/scripts/recent_sessions.py --repo-root <repo-root> --days 14 --limit 20`
   - session ID を指定されたら `--session-id <id>` を付けて先にその session を確認する。
3. Git 状態を集める。
   - `git status --short --branch`
   - `git worktree list --porcelain`
   - 各 worktree について `git -C <worktree> status --short --branch`
4. 必要なら変更範囲を比較する。
   - 進行中 branch の変更範囲: `git diff --name-only origin/main...<branch>`
   - local `main` に積まれた変更を前提にした比較: `git diff --name-only main...<branch>`
   - dirty worktree は `git -C <worktree> status --short` の変更ファイルを優先して見る。
5. session と worktree を対応付けて、重複と競合を判定する。
6. 安全な作業領域を提案する。ユーザが作成まで求めたら、その場で branch / worktree を作る。
7. `red`でも同じ所有セッションが続けるのが適切なら、新しい作業領域を作らず、後述の後続キューを使う。
8. 長期運用なら reservation ledger を作るか更新する。

# Conflict Levels

- `green`
  - 別 worktree で、対象ファイルと feature area が重ならない
- `yellow`
  - 同じファイルでも、変更するsymbol・責務・仕様が分離している
  - 同じ module や shared test / docs に触る
  - separate worktree、編集領域のownership、統合順序の明示が前提
- `red`
  - 同じbranchまたは同じworktreeを複数sessionで編集しようとしている
  - 同じ関数、型、プロパティ、または密接に結合したコード領域を変更する
  - 同じ仕様、責務、設計判断、またはfeatureを別sessionが進めている
  - 一方が対象ファイル全体の整形、分割、移動、生成を行う
  - dirtyなdetached worktreeが同じ編集領域を触っている

# Quick Reference

| State | Action |
| --- | --- |
| `green` | 独立した作業領域で進める |
| `yellow` | 別worktreeで編集領域と統合順序を明示して進める |
| `red`かつ既存所有セッションが続ける | ユーザーへ事前説明し、所有セッションの後続キューへ積む |
| `red`かつ所有者・scope・キュー動作が不明 | 送信も編集もせずユーザーへ確認する |

## Same-File Decision

同じファイルという事実は警告信号であり、それだけでは`red`にしない。

| Overlap | Level |
| --- | --- |
| 別の関数・型・責務を変更し、仕様上も独立している | `yellow` |
| 実装と、その変更領域に直接依存しないテストを変更する | `yellow` |
| 同じsymbol、密接に結合した挙動、同じ設計判断を変更する | `red` |
| ファイル全体の整形、分割、移動、生成が含まれる | `red` |
| 予定するsymbol・責務を特定できず、独立性を確認できない | scopeを明確にするまで`red` |

# Decision Rules

- 並列作業が quick review で終わらないなら、同じ worktree ではなく別 worktree を優先する。
- 新タスクが local `main` の未 push / 未 merge 変更に依存するなら、`origin/main` ではなく current `main` から切る。
- detached worktree は再利用しない。必要なら先に名前付き branch へ退避する。
- 同じファイルだけを理由に`red`へ分類しない。実際のdiffと予定するsymbol・責務・仕様を比較する。
- `red` 判定なら、勝手に作業を始めず競合点を明示して確認する。
- `yellow` 判定なら、別worktreeを使い、各sessionの編集領域と統合順序を先に言語化してから開始する。
- 同一ファイルを並行編集したbranchは、先に一方を統合し、他方を最新の基準branchへ追従させて差分確認と関連テストを行う。
- current task の編集symbol・責務が曖昧なら、独立性を確認できるまで`red`としてscopeを明確にする。

# Queueing Work For An Owning Session

`red` conflictで既存セッションが対象branch、編集領域、または設計責任を所有しており、そのセッションへ後続作業を渡す場合:

1. 対象セッション名とID、branch、worktree、競合ファイル、現在のturn状態を確認する。
2. 送信前に、競合の根拠、依頼先、依頼理由、現在のturnを中断せず後続キューへ積むことをユーザーへ伝える。承認済みscope内なら返答を待つ必要はない。
3. 対象セッションがactiveでもidleになるまで待たず、Codex appの`send_message_to_thread`など、現在のturnをinterruptしないfollow-up機構で今キューへ積む。
4. 受付結果の対象セッションIDを確認し、現在のturnが中断されていないことを`read_thread`または`wait_threads`で確認する。
5. ユーザーへ対象セッション名とID、キュー受付結果を報告する。受付は「後続依頼がキューに入った」証拠であり、着手や完了の証拠ではない。
6. 現在のturn完了後、新しいturnが開始したことを確認してから着手済みと報告する。
7. 正確な依頼先、非割り込みのキュー動作、または受付結果を確認できない場合は送信しない。別worktreeで同じ編集領域を編集せず、ユーザーへblockerを報告する。

## Queueing Red Flags

- ユーザーへ伝える前に別セッションへ送ろうとしている
- activeなセッションをinterruptして後続作業を優先しようとしている
- follow-upキューが使えるのに、idleになるまで送らず依頼忘れの余地を残している
- キュー受付を着手または完了として報告しようとしている
- 同じsymbol・責務・設計判断を別worktreeで並行編集しようとしている

## Queueing Rationalizations

| Rationalization | Required response |
| --- | --- |
| 「実行中に送ると現在のturnへ混ざりそうなのでidleまで待つ」 | 非割り込みのfollow-upキューを使い、現在のturnが継続していることを確認する。待機で代用しない。 |
| 「要件は承認済みなので、別セッションへ送ったことは後で報告すればよい」 | 承認済みでも、競合理由・依頼先・キュー投入を送信前に明示する。 |
| 「受付成功なら作業は始まったとみなせる」 | 受付はキュー登録のみ。新しいturnの開始を別に確認する。 |

# Reservation Ledger

複数 session を継続運用するなら、repo root の `.codex/parallel-session-ledger.md` を使う。

- 雛形: `/Users/tsonobe/.codex/skills/parallel-session-guard/references/ledger-template.md`
- 予約時に `session_id`, `worktree`, `branch`, `scope`, `reserved_paths`, `status` を追記する
- 終了時に `status` を `done` または `abandoned` に更新する
- ユーザが求めない限り commit 対象にはしない

# Stop And Ask

- 同じ編集領域、責務、またはfeatureを別sessionが触っており、既存所有セッションへ後続キューを積むのが適切か判断できない
- どの branch を基準に切るべきかで結論が変わる
- dirty な detached worktree を処理しないと安全な切り出しができない
- 既存の未 commit 変更を移動、stash、cleanup しないと進めない

# Reporting Format

結果は短く、次の順で返す。

1. 今の自分の作業とぶつかるか
2. 直近でアクティブな session / worktree
3. 重複または競合の根拠
4. 推奨する作業領域
5. 後続キューへ積んだ場合は、対象セッション名・ID・受付状態
6. 実際に作成した path / branch があればその場所

# Notes

- session の「active」は厳密な live 状態ではなく、最近のログ更新時刻で判断する
- session ログだけで scope が読めないときは、対応する worktree の Git 差分を優先する
- `main の作業を確認して` のような依頼では、session 指定がなくても recent session inventory と current `main` の commit / diff の両方で裏取りする

# Invocation

ユーザが次のように言ったら、この skill を使う。

- `parallel-session-guard で見て`
- `並列作業の衝突を避けたい`
- `active な session を棚卸しして`
- `競合しない worktree を用意して`
- `この task が今の main と重複しないか見て`
