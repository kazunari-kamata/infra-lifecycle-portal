from __future__ import annotations

from datetime import date

from app.backend.inventory import load_inventory_file
from app.backend.reporting import render_markdown_report
from app.backend.scanner import scan_inventory


def test_scan_inventory_classifies_lifecycle_risks() -> None:
    inventory = load_inventory_file("examples/inventory.yml")

    result = scan_inventory(inventory, today=date(2026, 4, 27))

    assert result.summary.total_servers == 3
    assert result.summary.total_findings == 12
    assert result.summary.high == 5
    assert result.summary.medium == 1
    assert result.summary.low == 1
    assert result.summary.info == 5
    assert result.findings[0].level.value == "HIGH"


def test_render_markdown_report_contains_sections() -> None:
    inventory = load_inventory_file("examples/inventory.yml")

    report = render_markdown_report(scan_inventory(inventory, today=date(2026, 4, 27)))

    assert "# インフラライフサイクルレポート" in report
    assert "## リスクサマリー" in report
    assert "api-01" in report
