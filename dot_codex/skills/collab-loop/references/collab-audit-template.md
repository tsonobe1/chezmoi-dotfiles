# Collab Audit Template

- 全 `it.todo` を提示したか: yes/no
- テストは構造化して提示したか: yes/no
- classical school / t-wada の観点で進めたか: yes/no
- `failure log status`: recorded / not-needed / missing
- `ADR status`: recorded / not-needed / missing
- 品質ゲートは通過したか: yes/no
- review finding dispositions: fixed / needs user confirmation / rejected by current constraint / not reproduced / deferred / n-a
- residual risk: none / listed

補足:

- 最終報告では `failure log: recorded/not-needed` か `ADR: recorded/not-needed` も別行で明示する。
- `failure log status` と `ADR status` は `Collab Audit` 用の集約値であり、上の別行を省略してよい意味ではない。
- subagent の validation failure は、親 session の official gate 結果と分けて書く。native ABI、process、permission、harness 差分が疑われる場合は、official gate で再現するまで product failure と断定しない。

例:

- `failure log status`: not-needed（再発防止に値する失敗がなかったため）
- `ADR status`: recorded（`docs/adr/2026-04-23-foo.md`）
- `review finding dispositions`: fixed=2, rejected by current constraint=1
- `residual risk`: listed（manual runtime smoke はユーザ確認待ち）
