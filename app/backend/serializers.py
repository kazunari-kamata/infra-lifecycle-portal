from __future__ import annotations

from app.backend.domain import ScanResult


def scan_result_to_dict(result: ScanResult) -> dict:
    return {
        "generated_at": result.generated_at,
        "inventory": {
            "service_name": result.inventory.service_name,
            "environment": result.inventory.environment,
            "owner": result.inventory.owner,
            "servers": [
                {
                    "hostname": server.hostname,
                    "role": server.role,
                    "os": _component_to_dict(server.os),
                    "middleware": [_component_to_dict(item) for item in server.middleware],
                    "runtimes": [_component_to_dict(item) for item in server.runtimes],
                }
                for server in result.inventory.servers
            ],
        },
        "summary": {
            "high": result.summary.high,
            "medium": result.summary.medium,
            "low": result.summary.low,
            "info": result.summary.info,
            "total_servers": result.summary.total_servers,
            "total_findings": result.summary.total_findings,
        },
        "findings": [
            {
                "level": finding.level.value,
                "server": finding.server,
                "role": finding.role,
                "component_type": finding.component_type,
                "component_name": finding.component_name,
                "version": finding.version,
                "eol_date": finding.eol_date.isoformat(),
                "days_to_eol": finding.days_to_eol,
                "summary": finding.summary,
                "recommendation": finding.recommendation,
            }
            for finding in result.findings
        ],
    }


def _component_to_dict(component) -> dict:
    return {
        "component_type": component.component_type,
        "name": component.name,
        "version": component.version,
        "eol": component.eol.isoformat(),
    }

