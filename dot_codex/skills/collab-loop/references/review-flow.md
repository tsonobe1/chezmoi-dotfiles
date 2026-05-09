# Review Flow

レビューのみ mode で読む。control line の後、本文は findings first にする。

## Priority

優先して確認する。

- 仕様との不一致
- 振る舞いのバグ
- 回帰リスク
- 契約違反（前提条件 / 事後条件 / 不変条件）
- テスト不足、誤ったテスト、保証対象のずれ
- 将来の実装判断に影響する設計判断の欠落

findings にしない。

- 単なる好みの差
- ユーザが求めていない大規模リファクタ提案
- 動作に影響しない軽微な stylistic nit

## Finding Shape

各 finding には次を含める。

- 何が問題か
- どこで起きるか（file / line）
- 何が壊れるか、またはどの保証が欠けるか
- なぜ current diff / current file contents からそう言えるか

レビューで新しい finding を返すときは、findings の後に短い説明を添える。

- `どう問題なのか`: 実際の操作やデータにどう悪影響が出るか
- `中学生にもわかる説明`: 専門用語を避け、身近な例で言い換える

## Historical Findings

ユーザが過去の review findings を貼っている場合:

1. 過去指摘を current fact として再掲しない。
2. current diff と current file contents で各指摘を `resolved` / `still valid` 判定する。
3. 新しい finding は、その判定後に別 finding として追加する。
4. `still valid` としたものには、同じ説明を付ける。

findings がない場合は `no findings` と明示し、residual risk または testing gap があれば短く添える。
