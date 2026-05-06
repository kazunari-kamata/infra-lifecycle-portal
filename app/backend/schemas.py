from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    inventory_text: str | None = Field(default=None)
    inventory: dict[str, Any] | None = Field(default=None)


class HealthResponse(BaseModel):
    status: str

