from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class RiskLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass(frozen=True)
class Component:
    component_type: str
    name: str
    version: str
    eol: date


@dataclass(frozen=True)
class Server:
    hostname: str
    role: str
    os: Component
    middleware: list[Component]
    runtimes: list[Component]


@dataclass(frozen=True)
class Inventory:
    service_name: str
    environment: str
    owner: str
    servers: list[Server]


@dataclass(frozen=True)
class Finding:
    level: RiskLevel
    server: str
    role: str
    component_type: str
    component_name: str
    version: str
    eol_date: date
    days_to_eol: int
    summary: str
    recommendation: str


@dataclass(frozen=True)
class ScanSummary:
    high: int
    medium: int
    low: int
    info: int
    total_servers: int
    total_findings: int


@dataclass(frozen=True)
class ScanResult:
    generated_at: str
    inventory: Inventory
    summary: ScanSummary
    findings: list[Finding]

