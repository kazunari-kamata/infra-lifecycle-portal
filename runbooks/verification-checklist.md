# Verification Checklist

## 変更前

- current inventory を確認済みであること。
- backup restore test の結果が確認できること。
- monitoring dashboard と alert path を確認済みであること。
- rollback owner が割り当て済みであること。

## 変更中

- service process が正常に起動すること。
- required port と upstream connectivity が正常であること。
- batch job と scheduler job を確認すること。
- error log に regression がないこと。

## 変更後

- synthetic test または manual application test が成功すること。
- business-critical transaction が正常に完了すること。
- metrics が合意済み baseline の範囲内にあること。
- change result と残課題を短く記録すること。
