---
name: empirical-prompt-tuning
description: Agent 向けテキスト指示（skill、slash command、task prompt、CLAUDE.md 節、コード生成プロンプト）を、白紙の subagent に実行させて両面評価し、改善が頭打ちになるまで反復改善する手法。Use when you need to harden a newly created or heavily revised instruction, or when an agent's poor behavior may be caused by ambiguity in the instruction itself rather than the task.
---

# Empirical Prompt Tuning

対象指示を自分で読み直して済ませない。固定したシナリオと要件チェックリストを先に決め、白紙の subagent を使って実測し、自己申告と指示側メトリクスの両面から改善点を詰める。

## モード

この skill は次の 2 モードを扱う。

- **execution tuning mode**: prompt や skill を白紙の subagent に実行させ、実行結果から改善する。重要度が高い対象では単一案ではなく候補群で回す
- **compliance audit mode**: 実タスクの transcript、diff、最終報告を監査し、対象 skill や prompt の遵守状況を点検する

曖昧なときは execution tuning mode を既定とし、`守られたか` を見たい依頼では compliance audit mode を使う。

## いつ使うか

- skill、slash command、task prompt を新規作成または大幅改訂した直後に使う
- エージェントの挙動が期待に届かず、原因が指示側の曖昧さにありそうなときに使う
- 頻繁に使う skill や自動化の中核プロンプトを堅牢化したいときに使う
- 実タスクの transcript を見て、skill の設計思想、hard gate、artifact 契約が本当に守られたか監査したいときに使う

次では使わない。

- 一回限りの使い捨てプロンプト
- 成功率ではなく書き手の好みだけを反映したいケース

## ワークフロー

0. **Iteration 0 — description と body の整合を静的に確認する**
   - frontmatter `description` の trigger と用途を読む
   - body が実際にカバーする範囲を読む
   - 乖離があれば iter 1 の前に `description` か body を合わせる
   - これを飛ばすと、subagent が description に合わせて body を補完し、false positive が出やすい
1. **ベースラインと候補群を準備する**
   - 評価シナリオを 2 から 3 本用意する。中央値 1 本、edge 1 から 2 本を目安にする
   - シナリオごとに要件チェックリストを 3 から 7 項目で固定する
   - チェックリストには `[critical]` 項目を最低 1 つ入れる
   - 通常は base prompt に加えて 1 から 3 個の変異候補を作り、候補群として評価する
   - 低コストで済ませたいときだけ単一候補で始める
2. **白紙の実行者に読ませる**
   - 新規 subagent を dispatch する
   - 同じ agent を再利用しない
   - 自己再読で代替しない
   - 複数シナリオや複数候補を同時に回すときは並列 dispatch する
3. **実行させる**
   - 後述の「subagent 起動契約」に従って対象プロンプト、シナリオ、要件チェックリストを渡す
   - 実行者には成果物の生成と自己申告レポートの返却を求める
   - 可能なら reasoning、tool calls、tool outputs を含む trajectory を要約して残す
4. **両面評価する**
   - 実行者の自己申告から、不明瞭点、裁量補完、再試行理由を抽出する
   - 指示側では成功/失敗、精度、steps、duration、retries を記録する
   - 成功判定は `[critical]` 項目がすべて ○ の場合に限る
   - 精度は `○ = 1.0`、`部分的 = 0.5`、`× = 0` で合算して算出する
   - 失敗した場合は、落ちた `[critical]` 項目を「不明瞭点」に 1 行で必ず残す
5. **Pareto frontier を残す**
   - 候補群のうち、他候補に一方的に負けていないものだけを残す
   - 少なくとも `[critical]` 成功、精度、steps、duration の 4 軸で非劣候補を判定する
   - best 1 本だけに早く絞らず、補完的な強みを持つ候補を 2 から 4 本残す
6. **lesson merge と最小差分を適用する**
   - frontier 上の候補から、効いた lesson を section 単位で抽出する
   - 競合しない lesson は merge 候補として 1 本に合成する
   - 1 イテレーション 1 テーマに絞る
   - 修正前に「この差分が要件チェックリストまたは判定文言のどれを満たすためのものか」を明示する
7. **新規 subagent で再評価する**
   - 前回と同じ agent を使い回さない
   - base、frontier 残存候補、merge 候補のどれを次イテレーションへ持ち越すかを明示する
   - 改善が頭打ちになるまで 2 から 6 を繰り返す
8. **収束を判定する**
   - 連続 2 イテレーションで新規不明瞭点ゼロかつ改善幅が閾値以下なら停止する
   - 重要度が高い指示では 3 連続を要求する

## GEPA-lite として守る核

この skill を GEPA 寄りに運用したいときは、少なくとも次を外さない。

- **trajectory-based reflection**: 出力の良し悪しだけでなく、実行過程から学ぶ
- **candidate population**: 毎回 1 本だけでなく 2 から 4 候補を持つ
- **Pareto retention**: 単一の best だけでなく非劣候補を残す
- **lesson merge**: 別候補で効いた改善を section 単位で合成する
- **hold-out check**: 訓練に使っていないシナリオで過適合を確認する

全部を満たさない場合でも empirical tuning ではあるが、GEPA-lite とは呼ばない。

## Compliance Audit Mode

このモードでは、対象 prompt を再実行するのではなく、既存 transcript や成果物から「守られたか」を監査する。

1. 対象 skill または prompt の契約を固定する
2. 監査対象を固定する。例: transcript、途中報告、`it.todo`、diff、最終報告
3. `[critical]` を含む compliance checklist を固定する
4. 白紙の subagent に、監査対象だけを渡して遵守状況を点検させる
5. `fulfilled / violated / partial` で項目ごとに判定させる
6. `violated / partial` が、対象 skill や prompt 自体の欠落なのか、十分な契約があるのに実運用が守れていないだけなのかを分ける
7. 新出 violation を潰す最小修正を skill か運用に入れる

このモードでは、「output が良かったか」より「必要な artifact と stop rule が見えたか」を重視する。
監査結果では少なくとも次を分ける。

- **instruction defect**: skill / prompt の文言、構造、判定基準、artifact 契約が不足している
- **operation defect**: skill / prompt には規定があるが、対象 run がそれを守れていない
  - 例: `Session Preamble` や `Compliance Checkpoint` を skill は要求しているのに、対象 transcript で実際には出ていない

## 評価軸

| 軸              | 取り方                                  | 意味                           |
| --------------- | --------------------------------------- | ------------------------------ |
| 成功/失敗       | `[critical]` 項目が全て ○ なら成功      | 最低ライン                     |
| 精度            | 要件チェックリストの達成率 %            | 部分成功の程度                 |
| ステップ数      | subagent 実行メタの `tool_uses`         | 指示の回り道の多さ             |
| 所要時間        | subagent 実行メタの `duration_ms`       | 認知負荷の代替指標             |
| 再試行回数      | 自己申告レポートから抽出                | 曖昧さのシグナル               |
| 不明瞭点        | 自己申告レポートから抽出                | 質的改善材料                   |
| 裁量補完        | 自己申告レポートから抽出                | 暗黙仕様の露出                 |
| 遵守率          | compliance checklist の達成率 %         | skill 契約の実運用での守られ方 |
| 違反件数        | hard gate / critical checklist の違反数 | 運用の破綻点                   |
| frontier 残存数 | 非劣候補として残った prompt 数          | 候補多様性の維持               |
| merge 改善率    | merge 候補が親候補平均を何点上回るか    | lesson 合成の効果              |

質的指標を主、量的指標を補助として扱う。時間短縮だけを最適化しない。

Codex では `spawn_agent` と結果待ちの応答メタを使って計測する。`tool_uses` や `duration_ms` が取得できない環境では `n/a` と明示し、成功/精度/質的フィードバックを主に回す。

compliance audit mode では、steps や duration よりも `critical` 違反と artifact 欠落を優先して扱う。

execution tuning mode で候補群を使う場合、単一候補の最速勝ちより frontier の質を優先する。

### `tool_uses` の質的解釈

- シナリオ間で `tool_uses` が他シナリオ比 3 から 5 倍以上に偏るなら、skill が decision-tree index 寄りで自己完結性が低い可能性が高い
- 典型例は、他シナリオが 1 から 3 なのに 1 本だけ 15 以上になるケース
- この偏りが出たら、冒頭に最小完成例や references を読む条件を足し、iter 2 を回す

精度 100% でも `tool_uses` の偏りが大きければ打ち切らない。

### Pareto retention の判定

候補 A が候補 B に支配されるのは、少なくとも次を満たすときとする。

- B が A と同じかそれ以上の `[critical]` 成功率を持つ
- B の精度が A 以上である
- B の steps と duration の少なくとも一方が A より良く、もう一方も悪化していない

支配されていない候補を frontier として残す。
迷う場合は候補を消しすぎず残す。

### lesson merge の規則

merge は何でも混ぜない。次だけを merge 対象にする。

- 対象 section が異なる改善
- 同じ判定文言に効いていても、文言が競合しない改善
- 親候補の両方で `[critical]` を壊していない改善

次は merge しない。

- 同じ section に対する相反する指示
- 精度は上がるが steps や ambiguity を大きく悪化させる改善
- 親候補の一方でしか成立していない局所ハック

### 修正の波及パターン

修正の効き方は線形ではない。次の 3 パターンを前提に扱う。

- **保守的に振れる**: 複数軸を狙ったのに 1 軸しか動かない
- **上振れする**: 1 つの構造的情報が複数軸に同時に効く
- **ゼロ振れする**: 軸名から推測した修正が判定文言に届かない

差分適用前に、「この修正が判定文言のどれを満たすか」を閾値文言レベルで言語化してから直す。

## subagent 起動契約

subagent には次の構造で依頼する。

```text
あなたは <対象プロンプト名> を白紙で読む実行者です。

## 対象プロンプト
<対象プロンプト全文を貼る or パスを渡して読ませる>

## シナリオ
<状況設定を 1 段落>

## 要件チェックリスト
1. [critical] <最低ライン>
2. <通常項目>
3. <通常項目>
...

## タスク
1. 対象プロンプトに従ってシナリオを実行し、成果物を生成する。
2. 終了時に下記レポート構造で返答する。

## レポート構造
- 成果物: <生成物 or 実行結果サマリ>
- 要件達成: 各項目について ○ / × / 部分的（理由付き）
- 不明瞭点: 詰まった箇所、解釈に迷った文言
- 裁量補完: 指示で決まっておらず自分の判断で埋めた箇所
- 再試行: 同じ判断をやり直した回数と理由
```

呼び出し側は、自己申告レポートと subagent 実行メタを集計して評価表を埋める。

## compliance audit mode の起動契約

監査 subagent には次の構造で依頼する。

```text
あなたは <対象 skill / prompt 名> の遵守監査者です。

## 対象契約
<対象 skill / prompt の relevant sections>

## 監査対象
<transcript、it.todo、diff、最終報告、checkpoint など>

## Compliance Checklist
1. [critical] <最低ライン>
2. <通常項目>
3. <通常項目>
...

## タスク
1. 監査対象が対象契約を満たしているか判定する。
2. fulfillment を `fulfilled / partial / violated` で返す。
3. violated または partial の根拠を、監査対象のどこから読めるか示す。

## レポート構造
- 監査結果サマリ: <総評>
- Checklist 判定: 各項目について fulfilled / partial / violated
- 判定種別: <instruction defect / operation defect / mixed>
- Critical violations: <あれば列挙>
- 欠落 artifact: <見えるべきだったのに無いもの>
- 裁量補完: <運用側が勝手に埋めていた箇所>
- 次の最小修正: <skill 修正 or 運用修正>
```

このモードでは transcript 全体を雑に渡さず、監査に必要な部分だけを渡す。

### compliance audit から skill 修正へ進むとき

compliance audit mode で skill 自体の最小修正案を出す場合、まずは対象 run の違反を `instruction defect` / `operation defect` / `mixed` に分類するだけでよい。修正を実際に適用する前に、次を明示する。

- 今回は `compliance audit + 最小修正案` で止めるのか
- 修正適用まで行うのか
- 修正後に execution tuning / hold-out check が必要な重要度か

### 作業後 reflection を instruction 改善へ戻すとき

実タスク後の反省を skill、AGENTS.md、prompt に反映する場合は、修正案の前に次を成果物として残す。

- source evidence: transcript 要約、diff、commit、review findings、ユーザー指摘のどれを根拠にしたか
- defect classification: 各反省点を `instruction defect` / `operation defect` / `mixed` に分類する
- target surface: 修正先を `skill` / `AGENTS.md` / `運用のみ` に分ける
- minimal wording proposal: 反映する場合の最小文言案
- not-applied list: 反映しない反省点と理由
- hold-out decision: 修正適用後に hold-out compliance audit が必要か

raw transcript がなく要約だけで監査する場合、artifact の存在は `fulfilled` にしない。repo で確認できる成果物、transcript 不在による推定、ユーザー報告からの推定を分け、該当項目は `partial` 以下として扱う。

頻繁に使う skill、hard gate、artifact 契約、subagent 起動契約、AGENTS.md の共通作業規約を変える場合は、修正後に新規 subagent で最低 1 本の hold-out compliance audit を行う。単発 run の運用ミスを記録するだけなら、hold-out は必須ではない。

既存 transcript の遵守監査だけなら execution tuning や hold-out は必須ではない。ただし、頻繁に使う skill、hard gate、artifact 契約、subagent 起動契約を変更する場合は、修正後に新規 subagent で最低 1 本の hold-out compliance audit を行う。GEPA-lite と呼ぶ場合は hold-out check を省略しない。

## 環境制約

新規 subagent を dispatch できない環境では empirical 評価を適用しない。

- 代替案 1: 親セッションのユーザーに別セッションを起動してもらう
- 代替案 2: `empirical evaluation skipped: dispatch unavailable` と明示報告する
- NG: 自己再読で代替する

**構造審査モード** を使う場合は、subagent に「今回は構造審査モードであり、実行ではなくテキスト整合性だけを見る」と明記する。構造審査は empirical の代替ではなく補助として扱う。

## 反復の打ち切り基準

### 収束

連続 2 回で次をすべて満たしたら停止する。

- 新規不明瞭点が 0 件
- 精度の前回比改善が +3 ポイント以下
- steps の前回比変動が ±10% 以内
- duration の前回比変動が ±15% 以内
- hold-out シナリオ 1 本を追加しても精度が直近平均から 15 ポイント以上落ちない

hold-out で 15 ポイント以上落ちるなら過適合なので、baseline シナリオ設計に戻って edge を足す。

### 発散

3 回以上回しても新規不明瞭点が減らないなら、修正パッチではなくプロンプト構造自体を書き直す。

### リソース打ち切り

改善コストと重要度が釣り合わなくなったら 80 点で止める。

## 提示フォーマット

各イテレーションは次で記録する。

```markdown
## Iteration N

### 変更点（前回差分）

- <修正内容 1 行>

### 候補群

| 候補 | 由来                       | 状態     |
| ---- | -------------------------- | -------- |
| P0   | base                       | frontier |
| P1   | mutation: trigger を明確化 | frontier |
| P2   | merge(P0, P1)              | dropped  |

### 実行結果（シナリオ別）

| 候補 | シナリオ | 成功/失敗 | 精度 | steps | duration | retries |
| ---- | -------- | --------- | ---- | ----- | -------- | ------- |
| P0   | A        | ○         | 90%  | 4     | 20s      | 0       |
| P1   | A        | ○         | 90%  | 6     | 24s      | 1       |
| P2   | B        | ×         | 60%  | 9     | 41s      | 2       |

### Frontier 判定

- 残す候補: `P0`, `P1`
- 落とす候補: `P2` — `P1` に支配される

### 不明瞭点（今回新出）

- <シナリオ B>: [critical] 項目 N が × — <落ちた理由 1 行>
- <シナリオ B>: <その他の指摘 1 行>
- <シナリオ A>: （新出なし）

### 裁量補完（今回新出）

- <シナリオ B>: <補完内容>

### Merge lesson

- `P0` から残す lesson: <1 行>
- `P1` から残す lesson: <1 行>
- 次の merge 候補: <1 行>

### 次の修正案

- <最小修正 1 行>

（収束判定: 連続 X 回クリア / 停止条件まであと Y 回）
```

compliance audit mode では、`成功/失敗` を `critical violations の有無` で判定し、`不明瞭点` の代わりに `違反点` と `欠落 artifact` を前に出す。
このとき、最終イテレーションの `violated` がそのまま「skill 修正が必要」を意味するとは限らない。更新後の skill が十分でも、監査シナリオの運用がまだ新ルールを満たしていなければ `operation defect` として扱う。

## Collab-Loop 監査の典型チェック

`collab-loop` を監査するときは、最低でも次を見る。

- `[critical]` task mode が最初に固定されている
- `[critical]` Session Preamble がある
- 実装タスクなら spec audit が `it.todo` より先にある
- `[critical]` `it.todo` 承認前に実装へ進んでいない
- `it.todo` と構造化テスト一覧が見える
- 最終報告に `failure log` と `ADR` の要否がある
- 実装タスクなら `Collab Audit` がある
- review / audit / implementation を同一役割で自己完結させていない

## Red Flags

| 合理化                                           | 実態                                               |
| ------------------------------------------------ | -------------------------------------------------- |
| 自分で読み直せば同じ効果がある                   | 客観視できない。必ず新規 subagent を dispatch する |
| 1 シナリオで十分                                 | 過適合する。最低 2 本、できれば 3 本               |
| 不明瞭点ゼロが 1 回出たから終わり                | 偶然を弾くために連続判定が必要                     |
| 複数の不明瞭点を一気に潰す                       | 何が効いたか分からなくなる                         |
| 微修正まで 1 件ずつ完全分離する                  | 1 テーマ単位でまとめるべきことまで分断してしまう   |
| メトリクスが良いから質的フィードバックは無視する | 痩せすぎたプロンプトを見逃す                       |
| 書き直した方が早い                               | 3 回以上減らないときだけ構造刷新に切り替える       |
| 同じ subagent を使い回す                         | 前回の改善を学習して汚染される                     |

## よくある失敗

- シナリオが楽すぎる、または難しすぎる
- 時間短縮だけを見て質的フィードバックを捨てる
- 1 イテレーションに無関係な変更を詰め込みすぎる
- 修正に合わせてシナリオ側を簡単にしてしまう

## 関連

- `superpowers:writing-skills` は skill 作成時の TDD アプローチに近い
- `retrospective-codify` はタスク完了後の学びの固定化に向く
- `superpowers:dispatching-parallel-agents` は複数シナリオを並列で回すときに併用する
