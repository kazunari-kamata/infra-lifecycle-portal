from __future__ import annotations

from pathlib import Path

from app.backend.main import app, health, scan
from app.backend.schemas import ScanRequest


def test_health_endpoint() -> None:
    paths = {route.path for route in app.routes}

    assert "/health" in paths
    assert health().model_dump() == {"status": "ok"}


def test_scan_endpoint() -> None:
    inventory_text = Path("examples/inventory.yml").read_text(encoding="utf-8")
    paths = {route.path for route in app.routes}

    payload = scan(ScanRequest(inventory_text=inventory_text))

    assert "/scan" in paths
    assert payload["summary"]["total_servers"] == 3
    assert any(item["level"] == "HIGH" for item in payload["findings"])
