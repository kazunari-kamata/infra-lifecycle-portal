from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.backend.inventory import load_inventory_text
from app.backend.scanner import scan_inventory
from app.backend.schemas import HealthResponse, ScanRequest
from app.backend.serializers import scan_result_to_dict

app = FastAPI(title="infra-lifecycle-portal", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/scan")
def scan(request: ScanRequest) -> dict:
    try:
        if request.inventory_text:
            inventory = load_inventory_text(request.inventory_text)
        elif request.inventory:
            inventory = load_inventory_text(json.dumps(request.inventory))
        else:
            raise ValueError("inventory_text または inventory のどちらかを指定してください。")
    except Exception as exc:  # pragma: no cover - FastAPI が HTTP response に変換します。
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return scan_result_to_dict(scan_inventory(inventory))
