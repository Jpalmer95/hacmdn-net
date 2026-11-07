"""Tool handlers for the HACMDN-Net Hermes Agent Plugin.

Every handler accepts `(args: dict, **kwargs) -> str`, catches all exceptions,
and returns a JSON string per the Hermes plugin compatibility contract.
"""

from __future__ import annotations

import json
from typing import Any

try:
    from .network import get_network
except ImportError:
    from network import get_network  # type: ignore[no-redef]


def hacmdn_route_query(args: dict[str, Any], **kwargs: Any) -> str:
    """Route a task/query through the HACMDN-Net neighborhood & escalation ladder."""
    try:
        query = str(args.get("query") or "").strip()
        if not query:
            return json.dumps({"error": "Parameter 'query' is required."})
        domain_hint = str(args.get("domain_hint") or "").strip()
        require_specialist_only = bool(args.get("require_specialist_only", False))
        allow_zerogpu_buffer = bool(args.get("allow_zerogpu_buffer", True))
        execute_live_model = bool(args.get("execute_live_model", True))

        net = get_network()
        result = net.route_query(
            query=query,
            domain_hint=domain_hint,
            require_specialist_only=require_specialist_only,
            allow_zerogpu_buffer=allow_zerogpu_buffer,
            execute_live_model=execute_live_model,
        )
        return json.dumps(result, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"hacmdn_route_query failed: {exc}"})


def hacmdn_publish_specialist(args: dict[str, Any], **kwargs: Any) -> str:
    """Validate via Eval-Before-Gossip and publish a specialist Capability Descriptor."""
    try:
        net = get_network()
        result = net.publish(args)
        return json.dumps(result, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"hacmdn_publish_specialist failed: {exc}"})


def hacmdn_bid_task(args: dict[str, Any], **kwargs: Any) -> str:
    """Run a Confidence-Weighted Bidding round across neighborhood specialists and connectors."""
    try:
        query = str(args.get("query") or "").strip()
        if not query:
            return json.dumps({"error": "Parameter 'query' is required."})
        domain_hint = str(args.get("domain_hint") or "").strip()
        include_proxy_bids = bool(args.get("include_proxy_bids", True))

        net = get_network()
        result = net.run_bidding_round(
            query=query,
            domain_hint=domain_hint,
            include_proxy_bids=include_proxy_bids,
        )
        return json.dumps(result, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"hacmdn_bid_task failed: {exc}"})


def hacmdn_bounty_flywheel(args: dict[str, Any], **kwargs: Any) -> str:
    """Manage the JIT Fine-Tuning Flywheel, Community Governance Votes, and Idle Compute Pool."""
    try:
        net = get_network()
        result = net.manage_flywheel(args)
        return json.dumps(result, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"hacmdn_bounty_flywheel failed: {exc}"})


def hacmdn_network_status(args: dict[str, Any], **kwargs: Any) -> str:
    """Inspect active neighborhoods, organizers, specialists, ZeroGPU buffer, and escrow receipts."""
    try:
        neighborhood_id = args.get("neighborhood_id")
        include_descriptors = bool(args.get("include_descriptors", True))
        net = get_network()
        result = net.status(
            neighborhood_id=str(neighborhood_id) if neighborhood_id else None,
            include_descriptors=include_descriptors,
        )
        return json.dumps(result, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"hacmdn_network_status failed: {exc}"})
