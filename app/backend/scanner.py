from __future__ import annotations

from datetime import date, datetime

from app.backend.domain import Finding, Inventory, RiskLevel, ScanResult, ScanSummary, Server


def scan_inventory(inventory: Inventory, today: date | None = None) -> ScanResult:
    reference_date = today or date.today()
    findings: list[Finding] = []

    for server in inventory.servers:
        findings.append(_build_finding(server, server.os, reference_date))
        findings.extend(_build_finding(server, component, reference_date) for component in server.middleware)
        findings.extend(_build_finding(server, component, reference_date) for component in server.runtimes)

    findings.sort(key=lambda item: (_level_rank(item.level), item.days_to_eol, item.server, item.component_name))
    summary = _build_summary(findings, len(inventory.servers))

    return ScanResult(
        generated_at=datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        inventory=inventory,
        summary=summary,
        findings=findings,
    )


def _build_finding(server: Server, component, reference_date: date) -> Finding:
    days_to_eol = (component.eol - reference_date).days
    level = _classify_risk(days_to_eol)

    if days_to_eol < 0:
        summary = f"{component.name} {component.version} は EOL を過ぎています。"
        recommendation = "次回の maintenance window までに、移行計画、検証範囲、rollback 準備を優先して整理してください。"
    elif days_to_eol <= 90:
        summary = f"{component.name} {component.version} は 90 日以内に EOL を迎えます。"
        recommendation = "実装計画を作成し、rollback 検証済みの change window を確保してください。"
    elif days_to_eol <= 180:
        summary = f"{component.name} {component.version} は 180 日以内に EOL を迎えます。"
        recommendation = "target platform、validation scope、dependency review を準備してください。"
    elif days_to_eol <= 365:
        summary = f"{component.name} {component.version} は 12 か月以内に EOL を迎えます。"
        recommendation = "migration backlog に登録し、upgrade path の作業量と影響範囲を見積もってください。"
    else:
        summary = f"{component.name} {component.version} は 12 か月以上 support 期間が残っています。"
        recommendation = "lifecycle date を継続管理し、次回の planning cycle で再確認してください。"

    return Finding(
        level=level,
        server=server.hostname,
        role=server.role,
        component_type=component.component_type,
        component_name=component.name,
        version=component.version,
        eol_date=component.eol,
        days_to_eol=days_to_eol,
        summary=summary,
        recommendation=recommendation,
    )


def _classify_risk(days_to_eol: int) -> RiskLevel:
    if days_to_eol <= 90:
        return RiskLevel.HIGH
    if days_to_eol <= 180:
        return RiskLevel.MEDIUM
    if days_to_eol <= 365:
        return RiskLevel.LOW
    return RiskLevel.INFO


def _level_rank(level: RiskLevel) -> int:
    return {
        RiskLevel.HIGH: 0,
        RiskLevel.MEDIUM: 1,
        RiskLevel.LOW: 2,
        RiskLevel.INFO: 3,
    }[level]


def _build_summary(findings: list[Finding], total_servers: int) -> ScanSummary:
    high = sum(1 for item in findings if item.level == RiskLevel.HIGH)
    medium = sum(1 for item in findings if item.level == RiskLevel.MEDIUM)
    low = sum(1 for item in findings if item.level == RiskLevel.LOW)
    info = sum(1 for item in findings if item.level == RiskLevel.INFO)
    return ScanSummary(
        high=high,
        medium=medium,
        low=low,
        info=info,
        total_servers=total_servers,
        total_findings=len(findings),
    )
