"""FastAPI backend routes for the HACMDN-Net Dashboard & Desktop Plugin (`/api/plugins/hacmdn/*`)."""

from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter

try:
    from ..network import get_network
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from network import get_network  # type: ignore[no-redef]

router = APIRouter()


@router.get("/hub")
async def get_hub_state() -> dict[str, Any]:
    """Return full Contributor Hub, hardware pools, anti-whale earnings, and network status."""
    def _load() -> dict[str, Any]:
        net = get_network()
        return {
            "hub": net.manage_contributor_hub({"action": "get_hub_snapshot"}),
            "network": net.status(include_descriptors=False),
        }

    return await asyncio.to_thread(_load)


@router.post("/action")
async def run_hub_action(body: dict[str, Any]) -> dict[str, Any]:
    """Execute a Contributor Hub, Worker Pool, or Bounty Flywheel action from the GUI."""
    def _exec() -> dict[str, Any]:
        net = get_network()
        kind = str(body.get("kind") or "hub").strip()
        if kind == "worker_pool":
            res = net.manage_worker_pool(body)
        elif kind == "flywheel":
            res = net.manage_flywheel(body)
        elif kind == "route":
            res = net.route_query(str(body.get("query") or ""))
        else:
            res = net.manage_contributor_hub(body)
        return {
            "ok": True,
            "result": res,
            "hub": net.manage_contributor_hub({"action": "get_hub_snapshot"}),
        }

    return await asyncio.to_thread(_exec)
