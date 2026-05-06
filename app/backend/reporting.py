from __future__ import annotations

from app.backend.domain import ScanResult


def render_markdown_report(result: ScanResult) -> str:
    lines = [
        "# インフラライフサイクルレポート",
        "",
        "## サービス概要",
        f"- サービス: {result.inventory.service_name}",
        f"- 環境: {result.inventory.environment}",
        f"- 担当: {result.inventory.owner}",
        f"- 生成日時: {result.generated_at}",
        "",
        "## リスクサマリー",
        f"- サーバー数: {result.summary.total_servers}",
        f"- 検出件数: {result.summary.total_findings}",
        f"- HIGH: {result.summary.high}",
        f"- MEDIUM: {result.summary.medium}",
        f"- LOW: {result.summary.low}",
        f"- INFO: {result.summary.info}",
        "",
        "## サーバーインベントリ",
        "| ホスト名 | 役割 | OS | Middleware | Runtimes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for server in result.inventory.servers:
        middleware = ", ".join(f"{item.name} {item.version}" for item in server.middleware) or "-"
        runtimes = ", ".join(f"{item.name} {item.version}" for item in server.runtimes) or "-"
        lines.append(
            f"| {server.hostname} | {server.role} | {server.os.name} {server.os.version} | {middleware} | {runtimes} |"
        )

    lines.extend(
        [
            "",
            "## 検出されたリスク",
            "| レベル | サーバー | コンポーネント種別 | コンポーネント | Version | EOL | EOL までの日数 | 概要 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for finding in result.findings:
        lines.append(
            "| "
            f"{finding.level.value} | "
            f"{finding.server} | "
            f"{finding.component_type} | "
            f"{finding.component_name} | "
            f"{finding.version} | "
            f"{finding.eol_date.isoformat()} | "
            f"{finding.days_to_eol} | "
            f"{finding.summary}"
            " |"
        )

    lines.extend(["", "## 推奨される次の対応", "1. `HIGH` の項目について migration priority を確認してください。"])
    lines.append("2. 180 日以内に EOL を迎える項目について、validation、rollback、maintenance window を調整してください。")
    lines.append("3. release cycle ごとに lifecycle date と application dependency の前提を見直してください。")
    return "\n".join(lines) + "\n"
