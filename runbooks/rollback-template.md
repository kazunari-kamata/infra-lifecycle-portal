# Rollback Template

## 変更概要

- Service:
- Change window:
- Change owner:
- Scope:

## Rollback 判断点

- irreversible な data change または schema change の前に戻せる最終地点:
- 判断に使う observability signal:
- rollback 中に許容できる最大停止時間:

## Rollback 手順

1. traffic change を停止し、追加の deployment activity を止めます。
2. 以前の compute instance、package set、または image に戻します。
3. 承認済み backup source から configuration と secrets を restore します。
4. service health、external connectivity、scheduled workload を確認します。
5. incident note と次の remediation step を記録します。

## 連絡先

- Technical lead:
- Business contact:
- Status update interval:
