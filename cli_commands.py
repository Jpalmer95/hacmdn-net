"""CLI and in-session slash commands for the HACMDN-Net Hermes Agent Plugin."""

from __future__ import annotations

import json
from typing import Any

try:
    from .network import get_network
except ImportError:
    from network import get_network  # type: ignore[no-redef]


def format_status_summary(status_data: dict[str, Any]) -> str:
    """Format a compact human-readable summary for `/hacmdn` and `hermes hacmdn status`."""
    lines = [
        f"=== {status_data['network_codename']} (v{status_data['spec_version']}) ===",
        f"HF Community Collection: {status_data['hf_community_collection']}",
        f"ZeroGPU Buffer Space:    {status_data['zerogpu_community_buffer']['url']}",
        f"Active Neighborhoods:    {len(status_data['neighborhoods'])}",
        f"Verified Specialists:    {status_data['specialists_count']}",
        f"Open Fine-Tune Bounties: {status_data['bounties_open']} / {status_data['bounties_total']}",
        f"Escrow Settled Credits:  {status_data['escrow_settled_credits']:.2f}",
        "",
        "Neighborhoods & Organizers:",
    ]
    for n in status_data["neighborhoods"]:
        lines.append(
            f"  • {n['neighborhood_id']} ({n['name']}) — Organizer: {n['organizer_id']} "
            f"[{n['organizer_model']}, stake={n['organizer_stake']}, rep={n['organizer_reputation']}]"
        )
    lines.append("")
    lines.append("Registered Micro-Specialists (Eval-Before-Gossip Verified):")
    for s in status_data["specialists"]:
        lines.append(
            f"  • {s['spec_id']} ({s['base_model']}) @ {s['neighborhood_id']} [{s['worker_status']}]\n"
            f"    Adapter: {s['adapter']} | Eval: {s['eval_score']:.2f} vs Base {s['base_model_score']:.2f} "
            f"(+{s['eval_margin']:.2f}) | Abstain >= {s['abstain_threshold']:.2f} | p95={s['p95_latency_ms']}ms"
        )
    return "\n".join(lines)


def handle_slash_command(raw_args: str, **kwargs: Any) -> str:
    """In-session `/hacmdn` slash command handler."""
    net = get_network()
    parts = (raw_args or "").strip().split(maxsplit=1)
    sub = parts[0].lower() if parts else "status"
    rest = parts[1] if len(parts) > 1 else ""

    if sub in ("help", "-h", "--help"):
        return (
            "Usage: /hacmdn [status | hub | pools | pitch <idea> | route <query> | bid <query> | bounties | vote <topic> | idle]\n"
            "  /hacmdn status          Show live neighborhoods, specialists, and ZeroGPU buffer\n"
            "  /hacmdn hub             Show your Contributor Hub: 70/10/10/10 earnings, Anti-Whale cap, & pitched ideas\n"
            "  /hacmdn pools           Profile hardware (Game-Guard) & show 4 work pools + Shortage Scores\n"
            "  /hacmdn pitch <idea>    Pitch a new community directive or niche specialist idea\n"
            "  /hacmdn route <query>   Route a task through the 6-tier escalation ladder\n"
            "  /hacmdn bid <query>     Run confidence-weighted bidding across specialists\n"
            "  /hacmdn bounties        List open JIT fine-tuning bounties & abstention gaps\n"
            "  /hacmdn vote <topic>    Cast a stake-weighted community directive vote\n"
            "  /hacmdn idle            Execute one productive idle-pool open-science task"
        )

    if sub == "status":
        return format_status_summary(net.status(include_descriptors=False))

    if sub in ("hub", "gui"):
        return json.dumps(net.manage_contributor_hub({"action": "export_gui_widget"}), indent=2)

    if sub == "pools":
        return json.dumps(net.manage_worker_pool({"action": "profile_and_recommend"}), indent=2)

    if sub == "pitch":
        if not rest:
            return "Usage: /hacmdn pitch <idea title>"
        return json.dumps(
            net.manage_contributor_hub({"action": "pitch_idea", "idea_title": rest, "idea_description": rest}),
            indent=2,
        )

    if sub == "route":
        if not rest:
            return "Usage: /hacmdn route <query>"
        return json.dumps(net.route_query(rest), indent=2)

    if sub == "bid":
        if not rest:
            return "Usage: /hacmdn bid <query>"
        return json.dumps(net.run_bidding_round(rest), indent=2)

    if sub == "bounties":
        return json.dumps(net.manage_flywheel({"action": "list_bounties"}), indent=2)

    if sub == "vote":
        topic = rest or "open-science-ligand-screening"
        return json.dumps(net.manage_flywheel({"action": "vote_directive", "directive_topic": topic}), indent=2)

    if sub == "idle":
        cat = rest if rest in ("open-science", "local-business-aid", "network-calibration") else "open-science"
        return json.dumps(net.manage_flywheel({"action": "run_idle_pool_task", "idle_pool_category": cat}), indent=2)

    # Treat arbitrary text as a routed query
    return json.dumps(net.route_query(raw_args.strip()), indent=2)


def setup_cli_parser(subparser: Any) -> None:
    """Configure `hermes hacmdn <subcommand>` argparse tree."""
    subs = subparser.add_subparsers(dest="hacmdn_subcommand")

    p_status = subs.add_parser("status", help="Show HACMDN-Net neighborhoods, specialists, and ZeroGPU buffer")
    p_status.add_argument("--json", action="store_true", help="Output raw JSON")

    p_route = subs.add_parser("route", help="Route a query through the 6-tier specialist escalation ladder")
    p_route.add_argument("query", nargs="+", help="Query string to route")
    p_route.add_argument("--domain", default="", help="Optional domain hint")
    p_route.add_argument("--strict", action="store_true", help="Require specialist only (no generalist fallback)")

    p_bid = subs.add_parser("bid", help="Run a confidence-weighted bidding round for a task")
    p_bid.add_argument("query", nargs="+", help="Task query to bid on")

    subs.add_parser("bounties", help="List JIT fine-tuning bounties, abstention gaps, and directive votes")

    p_sim = subs.add_parser("simulate", help="Run a multi-query neighborhood routing & abstention simulation")
    p_sim.add_argument("--json", action="store_true", help="Output JSON report")

    subs.add_parser("hub", help="Show Contributor & Node Operator Hub (earnings, Anti-Whale cap, pools, ideas)")
    subs.add_parser("pools", help="Profile local hardware (Game-Guard) and show Shortage Scores & 4 work pools")

    p_gui = subs.add_parser("gui", help="Export or serve the lightweight HACMDN-Net Contributor Hub GUI")
    p_gui.add_argument("--serve", action="store_true", help="Start local HTTP server on 127.0.0.1:8765")
    p_gui.add_argument("--port", type=int, default=8765, help="Port for --serve (default 8765)")

    subparser.set_defaults(func=handle_cli_command)


def handle_cli_command(args: Any) -> None:
    """Execute `hermes hacmdn <subcommand>`."""
    net = get_network()
    sub = getattr(args, "hacmdn_subcommand", None) or "status"

    if sub == "status":
        data = net.status(include_descriptors=bool(getattr(args, "json", False)))
        if getattr(args, "json", False):
            print(json.dumps(data, indent=2))
        else:
            print(format_status_summary(data))
        return

    if sub == "route":
        query_str = " ".join(getattr(args, "query", [])).strip()
        res = net.route_query(
            query=query_str,
            domain_hint=getattr(args, "domain", ""),
            require_specialist_only=bool(getattr(args, "strict", False)),
        )
        print(json.dumps(res, indent=2))
        return

    if sub == "bid":
        query_str = " ".join(getattr(args, "query", [])).strip()
        res = net.run_bidding_round(query=query_str)
        print(json.dumps(res, indent=2))
        return

    if sub == "bounties":
        res = net.manage_flywheel({"action": "list_bounties"})
        print(json.dumps(res, indent=2))
        return

    if sub == "hub":
        res = net.manage_contributor_hub({"action": "get_hub_snapshot"})
        print(json.dumps(res, indent=2))
        return

    if sub == "pools":
        res = net.manage_worker_pool({"action": "profile_and_recommend"})
        print(json.dumps(res, indent=2))
        return

    if sub == "gui":
        res = net.manage_contributor_hub({"action": "export_gui_widget"})
        if getattr(args, "serve", False):
            try:
                from .gui import serve_local_gui
            except ImportError:
                from gui import serve_local_gui  # type: ignore[no-redef]
            serve_local_gui(port=int(getattr(args, "port", 8765)))
            return
        print(json.dumps({"gui_widget_html_path": res.get("gui_widget_html_path"), "operator_id": res.get("operator_id"), "earnings_summary": res.get("earnings_summary")}, indent=2))
        return

    if sub == "simulate":
        trial_queries = [
            ("SQL Window Specialist Match", "Rewrite this PostgreSQL CTE query into a ROW_NUMBER() and LAG() window function over department_id"),
            ("JSON-RPC Tool Specialist Match", "Synthesize a strict JSON-RPC 2.0 tool call payload and Python signature for calculate_shipping_tariff"),
            ("Neighborhood Connector Triage", "Which neighborhood organizer and specialist handles PostgreSQL query rewriting vs JSON-RPC schema generation?"),
            ("Out-of-Domain Abstention & JIT Bounty Trigger", "Design a CRISPR Cas13 guide RNA for sorghum drought resistance with off-target thermodynamics"),
        ]
        results = []
        for label, q in trial_queries:
            r = net.route_query(q)
            results.append(
                {
                    "trial": label,
                    "query": q,
                    "status": r["status"],
                    "escalation_tier": r["escalation_tier"],
                    "escalation_label": r["escalation_label"],
                    "routed_to": r.get("routed_to"),
                    "confidence": r.get("confidence"),
                    "bounty_proposal": r.get("proposal"),
                }
            )
        print(json.dumps({"simulation_trials": results}, indent=2))
        return

    print(format_status_summary(net.status(include_descriptors=False)))
