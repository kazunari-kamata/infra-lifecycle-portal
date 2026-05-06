# 移行ポリシー

## リスク分類

- `HIGH`: EOL 済み、または EOL まで 90 日以内です。migration path、validation scope、rollback plan を優先して作成します。
- `MEDIUM`: EOL まで 180 日以内です。target version、dependency review、maintenance window の候補を整理します。
- `LOW`: EOL まで 365 日以内です。migration backlog に登録し、作業量と影響範囲を見積もります。
- `INFO`: EOL まで 365 日より長く残っています。定期的な planning cycle で継続確認します。

## 移行計画で確認すること

1. 影響を受ける server の業務重要度と maintenance 制約を確認します。
2. in-place upgrade、side-by-side replacement、platform migration のどれで進めるかを決めます。
3. 実装前に service validation の内容を定義します。
4. rollback の判断点と fallback path を準備します。
5. 変更後の verification evidence を記録します。

## 想定ユースケース

- application host の CentOS 7 から Rocky Linux / RHEL への移行
- application release cycle に合わせた runtime 更新
- vendor support を維持するための middleware upgrade
