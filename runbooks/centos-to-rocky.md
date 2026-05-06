# Runbook: CentOS から Rocky Linux への移行

## 目的

CentOS 7 host を Rocky Linux へ移行し、service continuity を維持しながら rollback checkpoint を明確にします。

## 前提条件

- inventory が最新で、application dependencies が確認済みであること。
- configuration と secrets の backup が取得済みであること。
- package repository、monitoring system、alert path への接続を確認済みであること。
- maintenance window と rollback owner が割り当て済みであること。

## 手順

1. configuration drift を止め、現行の package、service、mount 情報を取得します。
2. application data と configuration の restore 手順を確認します。
3. 同じ主要 software set を使い、non-production environment で移行手順を rehearsal します。
4. 同じ service role、firewall intent、monitoring hook を持つ Rocky Linux target を構築します。
5. application configuration と data を restore し、verification checklist を実行します。
6. controlled cutover により traffic を切り替えます。
7. 合意した observation window の間、log、latency、scheduled job を監視します。

## Rollback trigger

functional verification が失敗した場合、data integrity check が失敗した場合、または monitoring が合意済み threshold を超える継続的な劣化を示した場合に rollback を開始します。
