# インフラライフサイクルレポート

## サービス概要
- サービス: customer-portal-platform
- 環境: production
- 担当: Platform Operations
- 生成日時: 2026-04-27T02:48:04Z

## リスクサマリー
- サーバー数: 3
- 検出件数: 12
- HIGH: 5
- MEDIUM: 1
- LOW: 1
- INFO: 5

## サーバーインベントリ
| ホスト名 | 役割 | OS | Middleware | Runtimes |
| --- | --- | --- | --- | --- |
| api-01 | application | CentOS 7.9 | Nginx 1.20, PostgreSQL 13 | Python 3.9 |
| batch-01 | batch | Rocky Linux 8.10 | Apache HTTP Server 2.4 | Python 3.11, OpenJDK 17 |
| admin-01 | bastion | RHEL 8.10 | HAProxy 2.6 | Node.js 18, Ruby 3.2 |

## 検出されたリスク
| レベル | サーバー | コンポーネント種別 | コンポーネント | Version | EOL | EOL までの日数 | 概要 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HIGH | api-01 | os | CentOS | 7.9 | 2024-06-30 | -666 | CentOS 7.9 は EOL を過ぎています。 |
| HIGH | admin-01 | runtime | Node.js | 18 | 2025-04-30 | -362 | Node.js 18 は EOL を過ぎています。 |
| HIGH | api-01 | runtime | Python | 3.9 | 2025-10-31 | -178 | Python 3.9 は EOL を過ぎています。 |
| HIGH | api-01 | middleware | PostgreSQL | 13 | 2025-11-13 | -165 | PostgreSQL 13 は EOL を過ぎています。 |
| HIGH | admin-01 | runtime | Ruby | 3.2 | 2026-03-31 | -27 | Ruby 3.2 は EOL を過ぎています。 |
| MEDIUM | batch-01 | middleware | Apache HTTP Server | 2.4 | 2026-09-30 | 156 | Apache HTTP Server 2.4 は 180 日以内に EOL を迎えます。 |
| LOW | api-01 | middleware | Nginx | 1.20 | 2027-03-01 | 308 | Nginx 1.20 は 12 か月以内に EOL を迎えます。 |
| INFO | admin-01 | middleware | HAProxy | 2.6 | 2027-05-31 | 399 | HAProxy 2.6 は 12 か月以上 support 期間が残っています。 |
| INFO | batch-01 | runtime | Python | 3.11 | 2027-10-24 | 545 | Python 3.11 は 12 か月以上 support 期間が残っています。 |
| INFO | admin-01 | os | RHEL | 8.10 | 2029-05-31 | 1130 | RHEL 8.10 は 12 か月以上 support 期間が残っています。 |
| INFO | batch-01 | os | Rocky Linux | 8.10 | 2029-05-31 | 1130 | Rocky Linux 8.10 は 12 か月以上 support 期間が残っています。 |
| INFO | batch-01 | runtime | OpenJDK | 17 | 2029-09-30 | 1252 | OpenJDK 17 は 12 か月以上 support 期間が残っています。 |

## 推奨される次の対応
1. `HIGH` の項目について migration priority を確認してください。
2. 180 日以内に EOL を迎える項目について、validation、rollback、maintenance window を調整してください。
3. release cycle ごとに lifecycle date と application dependency の前提を見直してください。
