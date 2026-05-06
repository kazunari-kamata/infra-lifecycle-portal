# アーキテクチャ

## 概要

`infra-lifecycle-portal` は、inventory に記録された OS、middleware、runtime の EOL 情報を scan し、運用判断に使える形式で結果を返す構成です。

- `app/backend`: FastAPI entrypoint、YAML loader、scanner、Markdown report renderer、tests を配置します。
- `cli`: backend と同じ scan ロジックを Typer CLI として提供します。
- `app/frontend`: sample inventory を読み込み、backend の `/scan` に送信して結果を表示します。
- `examples`: sample inventory と生成済み report を配置します。
- `runbooks`: migration、rollback、verification の作業手順を配置します。

## 処理フロー

1. operator が YAML 形式の inventory を読み込みます。
2. backend が inventory を内部モデルへ変換します。
3. scanner が OS、middleware、runtime ごとに `days_to_eol` を計算します。
4. 残日数に応じて `HIGH`、`MEDIUM`、`LOW`、`INFO` に分類します。
5. 結果を CLI 出力、API JSON、Markdown report、dashboard 表示で確認します。

## 設計方針

- lifecycle 判定は読みやすさを優先し、複雑な rule engine は導入していません。
- inventory は repository 管理しやすい YAML としています。
- frontend は scan ロジックを持たず、結果の確認と共有に集中します。
- sample inventory は CentOS 7、runtime EOL、middleware support deadline など、実際の運用で起きやすい更新圧力を表現しています。
