# サービスコンセプト

## 目的

このプロジェクトは、インフラ lifecycle 管理のうち、以下の実務に近い範囲を扱います。

- EOL が障害要因になる前に可視化する
- inventory data を migration の検討材料に変換する
- scan 結果を verification と rollback 準備につなげる

対象は、小規模から中規模の運用チームが、まず手元の inventory からリスクを整理する場面です。

## 想定する使い方

1. service inventory を YAML に記録します。
2. CLI または API で scan を実行します。
3. operations、platform、application の関係者で結果を確認します。
4. `HIGH` の項目から migration plan、validation task、rollback を含む change window を検討します。

## 対象外

- CMDB の代替ではありません。
- asset discovery platform ではありません。
- migration の自動実行を行うものではありません。

このツールの役割は、lifecycle risk を早めに見える化し、変更作業の準備に進めることです。
