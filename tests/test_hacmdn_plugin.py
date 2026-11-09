"""Unit and integration test suite for the HACMDN-Net (`hacmdn`) Hermes Agent Plugin."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

import __init__ as plugin_root
import cli_commands
import network
import tools


@pytest.fixture(autouse=True)
def isolated_hacmdn_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Isolate every test against a fresh SQLite DB in tmp_path."""
    db_file = tmp_path / "test_hacmdn.db"
    monkeypatch.setenv("HACMDN_DB_PATH", str(db_file))
    network._NETWORK_INSTANCE = None
    yield db_file
    network._NETWORK_INSTANCE = None


class DummyPluginContext:
    def __init__(self) -> None:
        self.tools: dict[str, dict[str, Any]] = {}
        self.commands: dict[str, dict[str, Any]] = {}
        self.cli_commands: dict[str, dict[str, Any]] = {}
        self.skills: dict[str, Path] = {}

    def register_tool(self, name: str, toolset: str, schema: dict, handler: Any, emoji: str = "") -> None:
        self.tools[name] = {"toolset": toolset, "schema": schema, "handler": handler, "emoji": emoji}

    def register_command(self, name: str, handler: Any, description: str = "", args_hint: str = "") -> None:
        self.commands[name] = {"handler": handler, "description": description, "args_hint": args_hint}

    def register_cli_command(self, name: str, help: str, setup_fn: Any, handler_fn: Any) -> None:
        self.cli_commands[name] = {"help": help, "setup_fn": setup_fn, "handler_fn": handler_fn}

    def register_skill(self, name: str, path: Path) -> None:
        self.skills[name] = path


def test_plugin_registration():
    ctx = DummyPluginContext()
    plugin_root.register(ctx)
    assert set(ctx.tools.keys()) == {
        "hacmdn_route_query",
        "hacmdn_publish_specialist",
        "hacmdn_bid_task",
        "hacmdn_bounty_flywheel",
        "hacmdn_network_status",
        "hacmdn_worker_pool",
        "hacmdn_contributor_hub",
    }
    assert "hacmdn" in ctx.commands
    assert "hacmdn" in ctx.cli_commands
    assert "hacmdn-network" in ctx.skills
    assert ctx.skills["hacmdn-network"].is_file()


def test_network_status_seeded():
    res = json.loads(tools.hacmdn_network_status({}))
    assert res["network_codename"] == "HACMDN-Net"
    assert res["specialists_count"] == 3
    spec_ids = {s["spec_id"] for s in res["specialists"]}
    assert "qwen3-0.6b-neighborhood-connector-v1" in spec_ids
    assert "qwen3-0.6b-sql-window-rewriter-v1" in spec_ids
    assert "qwen3-0.6b-json-rpc-tool-caller-v1" in spec_ids


def test_eval_before_gossip_rejects_low_margin_and_unapproved_base():
    # 1. Unapproved base model family -> rejected (Principle 4)
    bad_base = json.loads(
        tools.hacmdn_publish_specialist(
            {
                "spec_id": "llama-random-specialist",
                "base_model": "meta-llama/Llama-3-8B",
                "task_descriptor": "Random non-Qwen base model",
                "domains": ["sql"],
                "eval_score": 0.90,
                "base_model_score": 0.30,
            }
        )
    )
    assert bad_base["accepted"] is False
    assert bad_base["reason"] == "unapproved_base_model"

    # 2. Insufficient eval margin (< +0.15 over base) -> rejected (Principle 5)
    low_margin = json.loads(
        tools.hacmdn_publish_specialist(
            {
                "spec_id": "qwen3-0.6b-weak-sql",
                "base_model": "Qwen/Qwen3-0.6B",
                "task_descriptor": "Weak SQL model that barely beats base",
                "domains": ["sql"],
                "eval_score": 0.38,
                "base_model_score": 0.31,
            }
        )
    )
    assert low_margin["accepted"] is False
    assert low_margin["reason"] == "failed_eval_before_gossip"

    # 3. Valid specialist beating base by >= 0.15 -> accepted & gossiped
    good = json.loads(
        tools.hacmdn_publish_specialist(
            {
                "spec_id": "qwen3-0.6b-Systemd-Unit-Auditor-v1",
                "base_model": "Qwen/Qwen3-0.6B",
                "task_descriptor": "Audits Linux systemd service units and Tailscale firewall bindings",
                "domains": ["devops", "systemd", "tailscale"],
                "eval_score": 0.89,
                "base_model_score": 0.29,
                "abstain_threshold": 0.63,
            }
        )
    )
    assert good["accepted"] is True
    assert good["verified_on_entry"] is True
    assert good["eval_margin"] == pytest.approx(0.60)
    assert good["descriptor"]["diversity_fingerprint"].startswith("divfp:v1:")


def test_bidding_and_routing_sql_and_json_rpc():
    # SQL Window Function routing
    sql_route = json.loads(
        tools.hacmdn_route_query(
            {
                "query": "Rewrite this PostgreSQL CTE query with PARTITION BY department_id into a ROW_NUMBER and LAG window function",
            }
        )
    )
    assert sql_route["status"] == "ok"
    assert sql_route["routed_to"] == "qwen3-0.6b-sql-window-rewriter-v1"
    assert sql_route["confidence"] >= sql_route["abstain_threshold"]
    assert "OVER (PARTITION BY" in sql_route["output"]
    assert sql_route["settlement_receipt"]["escrow_credits"] > 0

    # JSON-RPC Tool Call synthesis routing
    rpc_route = json.loads(
        tools.hacmdn_route_query(
            {
                "query": "Synthesize a JSON-RPC 2.0 tool_call payload and Python function signature for calculate_rebate",
            }
        )
    )
    assert rpc_route["status"] == "ok"
    assert rpc_route["routed_to"] == "qwen3-0.6b-json-rpc-tool-caller-v1"
    assert json.loads(rpc_route["output"])["jsonrpc"] == "2.0"

    # Bidding round includes both direct worker bids and Neighborhood Connector proxy bids
    bids = json.loads(
        tools.hacmdn_bid_task(
            {
                "query": "Rewrite PostgreSQL CTE into window function",
                "include_proxy_bids": True,
            }
        )
    )
    bid_types = {b["bid_type"] for b in bids["ranked_bids"]}
    assert "direct_worker_bid" in bid_types
    assert "connector_proxy_bid" in bid_types


def test_zerogpu_community_buffer_escalation():
    # Publish a specialist whose local P2P node is offline (`zerogpu_buffered`)
    tools.hacmdn_publish_specialist(
        {
            "spec_id": "qwen3-0.6b-devops-traefik-v1",
            "base_model": "Qwen/Qwen3-0.6B",
            "task_descriptor": "Generates Traefik dynamic YAML and Docker container routing rules",
            "domains": ["devops", "traefik", "docker"],
            "eval_score": 0.91,
            "base_model_score": 0.30,
            "worker_status": "zerogpu_buffered",
        }
    )
    routed = json.loads(
        tools.hacmdn_route_query(
            {
                "query": "Generate a Traefik dynamic YAML router for a Docker container on port 3002",
                "domain_hint": "devops",
                "allow_zerogpu_buffer": True,
            }
        )
    )
    assert routed["status"] == "ok"
    assert routed["escalation_tier"] == 3
    assert routed["served_via"] == "jkorstad/hacmdn-community-buffer"


def test_out_of_domain_abstention_opens_jit_bounty():
    ood = json.loads(
        tools.hacmdn_route_query(
            {
                "query": "Calculate the orbital perturbation of a retrograde Trojan asteroid under Jupiter J2 harmonics",
                "require_specialist_only": True,
            }
        )
    )
    assert ood["status"] == "abstain"
    assert ood["escalation_tier"] == 5
    assert "proposal" in ood
    bounty_id = ood["proposal"]["bounty_id"]
    assert bounty_id.startswith("bounty-")

    # Claim and fulfill the bounty through the JIT Fine-Tuning Flywheel
    claim = json.loads(
        tools.hacmdn_bounty_flywheel(
            {
                "action": "claim_bounty",
                "bounty_id": bounty_id,
                "contributor_id": "jkorstad-rtx4070ti",
            }
        )
    )
    assert claim["claimed_by"] == "jkorstad-rtx4070ti"

    submit = json.loads(
        tools.hacmdn_bounty_flywheel(
            {
                "action": "submit_bounty_adapter",
                "bounty_id": bounty_id,
                "eval_score": 0.90,
                "base_model_score": 0.28,
            }
        )
    )
    assert submit["status"] == "fulfilled_and_paid"
    assert submit["published_specialist"]["accepted"] is True


def test_governance_vote_and_idle_pool_and_slash_command():
    vote = json.loads(
        tools.hacmdn_bounty_flywheel(
            {
                "action": "vote_directive",
                "directive_topic": "open-science-antimalarial-docking",
                "contributor_id": "jkorstad",
            }
        )
    )
    assert vote["total_weight"] > 0

    idle = json.loads(
        tools.hacmdn_bounty_flywheel(
            {
                "action": "run_idle_pool_task",
                "idle_pool_category": "local-business-aid",
            }
        )
    )
    assert idle["status"] == "completed_and_verified"
    assert idle["credits_earned"] > 0

    slash_out = cli_commands.handle_slash_command("status")
    assert "HACMDN-Net" in slash_out
    assert "qwen3-0.6b-neighborhood-connector-v1" in slash_out


def test_worker_pool_and_anti_whale_contributor_hub(tmp_path: Path):
    # 1. Profile hardware & recommend specialist by Shortage Score
    prof = json.loads(tools.hacmdn_worker_pool({"action": "profile_and_recommend"}))
    assert "hardware_profile" in prof
    assert len(prof["shortage_rankings"]) >= 3

    # 2. Run parallel batch across mesh work pool
    batch = json.loads(
        tools.hacmdn_worker_pool(
            {
                "action": "run_parallel_batch",
                "batch_queries": [
                    "Rewrite PostgreSQL CTE into ROW_NUMBER() OVER window function",
                    "Synthesize JSON-RPC 2.0 tool call for calculate_shipping",
                ],
            }
        )
    )
    assert batch["subtasks_count"] == 2
    assert batch["results"][0]["status"] == "ok"

    # 3. Pitch a new community idea
    idea = json.loads(
        tools.hacmdn_contributor_hub(
            {
                "action": "pitch_idea",
                "idea_title": "Local Farm-to-Table Supply Chain Schema Normalizer",
                "idea_category": "local-business-aid",
            }
        )
    )
    assert idea["status"] == "community_voting"
    assert idea["initial_vote_weight"] > 0

    # 4. Simulate Datacenter Overflow (120.0 raw credits -> capped at 50.0, 70.0 overflow to Community Pool)
    overflow = json.loads(
        tools.hacmdn_contributor_hub(
            {
                "action": "simulate_datacenter_overflow",
                "raw_datacenter_credits": 120.0,
            }
        )
    )
    assert overflow["datacenter_personal_payout"] == 50.0
    assert overflow["philanthropic_overflow_to_community_pool"] == 70.0
    assert overflow["small_operator_dividend_boost"]["dividend_added_credits"] == 35.0

    # 5. Export GUI Hub HTML widget
    hub = json.loads(tools.hacmdn_contributor_hub({"action": "export_gui_widget"}))
    assert Path(hub["gui_widget_html_path"]).is_file()
    assert hub["earnings_summary"]["total_accumulated_credits"] > 35.0


def test_phase6_rendezvous_gguf_daemon_and_iroh_p2p_gossip():
    # v0.4: Outbound HTTPS/WSS Rendezvous Work-Queue & llama.cpp GGUF+LoRA Hot-Swap Daemon
    rv = json.loads(
        tools.hacmdn_worker_pool(
            {
                "action": "sync_rendezvous_daemon",
                "enqueue_query": "Rewrite correlated SQL subquery into SUM(amount) OVER (PARTITION BY customer_id)",
            }
        )
    )
    assert rv["action"] == "sync_rendezvous_daemon"
    assert rv["lease_id"] == "lease-jkorstad-node-01"
    assert rv["tasks_drained_count"] >= 2
    assert rv["llama_cpp_daemon"]["hot_swaps_in_tick"] >= 1
    assert "Qwen3-0.6B-Q4_K_M.gguf" in rv["llama_cpp_daemon"]["gguf_resident_base"]

    # v0.6: Iroh QUIC P2P Hole-Punching & Content-Addressed BLAKE3 LoRA Blob Gossip
    p2p = json.loads(
        tools.hacmdn_worker_pool(
            {
                "action": "gossip_and_holepunch_p2p",
                "spec_id": "qwen3-0.6b-sql-window-rewriter-v1",
            }
        )
    )
    assert p2p["action"] == "gossip_and_holepunch_p2p"
    assert p2p["direct_quic_peers_count"] >= 2
    assert p2p["derp_relay_fallback_peers_count"] >= 1
    assert p2p["gossiped_lora_blob"]["blob_cid"].startswith("blake3:")
    assert p2p["gossiped_lora_blob"]["chunks_integrity_verified"] is True


def test_phase6_execution_verified_distillation_factory_and_l402_settlement():
    # v0.5: Execution-Verified Synthetic Distillation Factory + 40% Hard-Negative/OOD DPO
    distill = json.loads(
        tools.hacmdn_bounty_flywheel(
            {
                "action": "distill_bounty",
                "bounty_id": "bounty-sqlite-to-duckdb-v1",
                "auto_submit": True,
            }
        )
    )
    assert distill["action"] == "distill_bounty"
    assert distill["bounty_status"] == "fulfilled_and_paid"
    rep = distill["distillation_report"]
    vs = rep["verification_summary"]
    assert vs["candidates_verified"] >= 5
    assert vs["candidates_rejected_by_verifier"] >= 2
    assert vs["dpo_preference_pairs_count"] >= 4
    assert rep["passes_eval_before_gossip"] is True
    assert Path(rep["curriculum_json_path"]).is_file()

    # v1.0: L402 Lightning Micropayment Macaroon + Preimage Settlement & Verification
    l402 = json.loads(
        tools.hacmdn_contributor_hub(
            {
                "action": "settle_l402_and_dividends",
                "sats_per_credit": 100,
            }
        )
    )
    assert l402["action"] == "settle_l402_and_dividends"
    assert l402["status"] == "settled_verified"
    assert l402["preimage_sha256_verified"] is True
    assert l402["sats_settled"] >= 700
    assert l402["authorization_header"].startswith("L402 macaroon:v1:")

    verify = json.loads(
        tools.hacmdn_contributor_hub(
            {
                "action": "verify_l402_receipt",
                "settlement_id": l402["settlement_id"],
            }
        )
    )
    assert verify["verified"] is True
    assert verify["payment_hash"] == l402["payment_hash"]

