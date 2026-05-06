from __future__ import annotations

from pathlib import Path

import typer

from app.backend.inventory import load_inventory_file
from app.backend.reporting import render_markdown_report
from app.backend.scanner import scan_inventory
from app.backend.serializers import scan_result_to_dict

cli = typer.Typer(help="インフラ lifecycle risk を scan します。")


@cli.command()
def scan(inventory_path: str) -> None:
    """inventory file を scan し、summary を表示します。"""
    result = scan_inventory(load_inventory_file(inventory_path))
    payload = scan_result_to_dict(result)

    typer.echo(f"サービス: {payload['inventory']['service_name']}")
    typer.echo(f"環境: {payload['inventory']['environment']}")
    typer.echo(f"サーバー数: {payload['summary']['total_servers']}")
    typer.echo(
        "リスクサマリー: "
        f"HIGH={payload['summary']['high']} "
        f"MEDIUM={payload['summary']['medium']} "
        f"LOW={payload['summary']['low']} "
        f"INFO={payload['summary']['info']}"
    )
    typer.echo("")
    for finding in payload["findings"]:
        typer.echo(
            f"[{finding['level']}] {finding['server']} "
            f"{finding['component_type']} {finding['component_name']} {finding['version']} "
            f"(EOL {finding['eol_date']}, 残日数 {finding['days_to_eol']})"
        )


@cli.command()
def report(inventory_path: str, output: str = typer.Option(..., "--output", "-o")) -> None:
    """inventory file から Markdown report を生成します。"""
    result = scan_inventory(load_inventory_file(inventory_path))
    report_text = render_markdown_report(result)
    output_path = Path(output)
    output_path.write_text(report_text, encoding="utf-8")
    typer.echo(f"レポートを書き出しました: {output_path}")


if __name__ == "__main__":
    cli()
