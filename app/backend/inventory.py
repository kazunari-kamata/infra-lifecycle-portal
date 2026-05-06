from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from app.backend.domain import Component, Inventory, Server


def load_inventory_file(path: str | Path) -> Inventory:
    with Path(path).open("r", encoding="utf-8") as handle:
        return load_inventory_text(handle.read())


def load_inventory_text(raw_text: str) -> Inventory:
    payload = yaml.safe_load(raw_text)
    if not isinstance(payload, dict):
        raise ValueError("inventory の root は mapping である必要があります。")

    metadata = payload.get("service", {})
    servers_payload = payload.get("servers", [])
    if not isinstance(servers_payload, list):
        raise ValueError("inventory の 'servers' は list である必要があります。")

    servers = [_parse_server(item) for item in servers_payload]
    return Inventory(
        service_name=str(metadata.get("name", "名称未設定サービス")),
        environment=str(metadata.get("environment", "unknown")),
        owner=str(metadata.get("owner", "unknown")),
        servers=servers,
    )


def _parse_server(payload: dict) -> Server:
    return Server(
        hostname=str(payload["hostname"]),
        role=str(payload.get("role", "unknown")),
        os=_parse_component("os", payload["os"]),
        middleware=[_parse_component("middleware", item) for item in payload.get("middleware", [])],
        runtimes=[_parse_component("runtime", item) for item in payload.get("runtimes", [])],
    )


def _parse_component(component_type: str, payload: dict) -> Component:
    return Component(
        component_type=component_type,
        name=str(payload["name"]),
        version=str(payload.get("version", "unknown")),
        eol=date.fromisoformat(str(payload["eol"])),
    )
