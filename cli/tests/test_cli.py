from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_scan_command() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "cli.ilp", "scan", "examples/inventory.yml"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "リスクサマリー:" in completed.stdout
    assert "[HIGH]" in completed.stdout


def test_report_command(tmp_path: Path) -> None:
    output = tmp_path / "report.md"

    completed = subprocess.run(
        [sys.executable, "-m", "cli.ilp", "report", "examples/inventory.yml", "--output", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "レポートを書き出しました" in completed.stdout
    assert output.exists()
    assert "インフラライフサイクルレポート" in output.read_text(encoding="utf-8")
