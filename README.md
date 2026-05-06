# infra-lifecycle-portal

`infra-lifecycle-portal` は、OS、middleware、language runtime のライフサイクルリスクを確認し、移行計画、検証、rollback 準備につなげるための小さな infrastructure lifecycle 管理ツールです。

単なるデモではなく、CentOS から Rocky Linux / RHEL への移行、middleware の EOL 対応、runbook に基づく変更作業を意識した構成にしています。

## 目的

このリポジトリは、以下を確認できる実行可能なサンプルです。

- YAML の inventory から lifecycle risk を検出する
- OS、middleware、runtime の EOL 状況を `HIGH`、`MEDIUM`、`LOW`、`INFO` で分類する
- CLI、FastAPI、React dashboard から同じ scan ロジックを利用する
- Markdown report、runbook、verification checklist、rollback template を残す
- Docker Compose と GitHub Actions でローカル実行と CI を確認する

## 主な機能

- `examples/inventory.yml` の読み込み
- OS、middleware、runtime の EOL リスク判定
- Markdown report 生成
- Typer による CLI
- `GET /health` と `POST /scan` を提供する FastAPI backend
- sample inventory を読み込んで結果を表示する React + TypeScript frontend
- backend / frontend を起動する Docker Compose
- backend tests と CLI tests を実行する GitHub Actions CI

## ディレクトリ構成

```text
infra-lifecycle-portal/
├── README.md
├── AGENTS.md
├── docs/
│   ├── architecture.md
│   ├── migration-policy.md
│   └── service-concept.md
├── app/
│   ├── backend/
│   └── frontend/
├── cli/
│   ├── ilp.py
│   └── tests/
├── examples/
│   ├── inventory.yml
│   └── report-sample.md
├── runbooks/
│   ├── centos-to-rocky.md
│   ├── rollback-template.md
│   └── verification-checklist.md
├── .github/
│   └── workflows/
└── docker-compose.yml
```

## ローカルセットアップ

Python 3.12 を想定しています。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r app/backend/requirements.txt
python -m pip install -r cli/requirements.txt
```

## CLI の使い方

sample inventory を scan します。

```bash
python -m cli.ilp scan examples/inventory.yml
```

Markdown report を生成します。

```bash
python -m cli.ilp report examples/inventory.yml --output examples/report-sample.md
```

## API の使い方

backend を起動します。

```bash
uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
```

health check:

```bash
curl http://localhost:8000/health
```

sample inventory を scan します。

```bash
python - <<'PY'
from pathlib import Path
import json
import urllib.request

payload = json.dumps({
    "inventory_text": Path("examples/inventory.yml").read_text(encoding="utf-8")
}).encode("utf-8")

request = urllib.request.Request(
    "http://localhost:8000/scan",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request) as response:
    print(response.read().decode("utf-8"))
PY
```

## Frontend の使い方

```bash
cd app/frontend
npm install
npm run dev -- --host 0.0.0.0
```

frontend は既定で `http://localhost:8000` の backend に接続します。接続先を変更する場合は `VITE_API_BASE` を指定してください。

Node.js / npm がない環境では、Docker で npm command を実行できます。

```bash
./scripts/npm-docker.sh install
./scripts/npm-docker.sh run build
```

Dockerfile の buildcheck target でも frontend build を確認できます。

```bash
docker build --target buildcheck -f app/frontend/Dockerfile .
```

## Docker Compose

```bash
docker compose up --build
```

起動後に以下へアクセスします。

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

`docker compose up --build` はログに attach したまま動き続けます。バックグラウンドで起動したい場合は次のように実行します。

```bash
docker compose up -d --build
```

停止する場合:

```bash
docker compose down
```

## テスト

```bash
python -m pytest app/backend/tests cli/tests
```

## GitHub Actions CI

CI は `push` と `pull_request` で実行されます。

実行内容:

- Python 3.12 のセットアップ
- backend / CLI dependencies のインストール
- `python -m pytest app/backend/tests cli/tests`
- `python -m cli.ilp scan examples/inventory.yml`
- `python -m cli.ilp report examples/inventory.yml --output /tmp/report-sample.md`
- Node.js 22 のセットアップ
- `app/frontend` で `npm install`
- `app/frontend` で `npm run build`

同じ確認をローカルで実行する場合:

```bash
python -m pip install -r app/backend/requirements.txt
python -m pip install -r cli/requirements.txt
python -m pytest app/backend/tests cli/tests
python -m cli.ilp scan examples/inventory.yml
python -m cli.ilp report examples/inventory.yml --output /tmp/report-sample.md

cd app/frontend
npm install
npm run build
```

## CLI 出力例

```text
サービス: customer-portal-platform
環境: production
サーバー数: 3
リスクサマリー: HIGH=5 MEDIUM=1 LOW=1 INFO=5
```

Markdown report の例は `examples/report-sample.md` にあります。

## 補足

このプロジェクトは、lifecycle date、migration sequence、validation scope、rollback criteria など、インフラ変更作業で必要になる観点を小さくまとめたものです。製品としての完成度を主張するものではなく、実務で扱う判断材料をコードとドキュメントで表現することを目的にしています。
