"""Lightweight Optional GUI Hub & Inline Preview Widget for HACMDN-Net (`hacmdn`).

Provides:
  1. `write_hub_preview_html(snapshot)` — generates a self-contained, theme-aware HTML
     widget (using Hermes Desktop `--foreground`, `--muted-foreground`, `--accent`,
     `--border`, `--card` variables and `data-hermes-send` interactive actions).
  2. `serve_local_gui(port=8765)` — zero-dependency loopback HTTP server (`127.0.0.1`)
     for standalone CLI users (`hermes hacmdn gui --serve`).
"""

from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Optional


def render_hub_html(snapshot: dict[str, Any]) -> str:
    """Render the Contributor & Node Operator Hub HTML widget."""
    op_id = html.escape(str(snapshot.get("operator_id", "jkorstad-node-01")))
    earn = snapshot.get("earnings_summary") or {}
    policy = snapshot.get("anti_whale_policy") or {}
    wh = snapshot.get("worker_and_hardware") or {}
    hw = wh.get("hardware_profile") or {}
    wstate = wh.get("worker_state") or {}
    ideas = snapshot.get("ideas_pitched") or []
    bounties = snapshot.get("open_bounties") or []
    shortage = wh.get("shortage_rankings") or []

    total_cr = float(earn.get("total_accumulated_credits", 0.0))
    worker_cr = float(earn.get("worker_inference_credits_capped", 0.0))
    royalty_cr = float(earn.get("adapter_author_royalty_credits", 0.0))
    conn_cr = float(earn.get("connector_routing_credits", 0.0))
    div_cr = float(earn.get("community_dividend_pool_credits", 0.0))
    cap_pct = float(earn.get("cap_utilization_pct", 0.0))
    daily_cap = float(policy.get("daily_personal_cap_credits", 50.0))
    overflow_pool = float(policy.get("network_datacenter_overflow_pool_credits", 0.0))
    tasks_done = int(earn.get("tasks_completed", 0))
    tokens_done = int(earn.get("tokens_contributed", 0))

    pools_html = ""
    for p in hw.get("work_pools") or []:
        badge_bg = "rgba(34,197,94,0.16)" if p.get("status") == "subscribed" else "rgba(148,163,184,0.15)"
        badge_fg = "#22c55e" if p.get("status") == "subscribed" else "var(--muted-foreground)"
        pools_html += f"""
        <div class="row-item">
          <div>
            <div class="item-title">{html.escape(str(p.get("name", "")))}</div>
            <div class="item-sub">{html.escape(str(p.get("pool_id", "")))} · {html.escape(str(p.get("target_models", "")))}</div>
          </div>
          <span class="pill" style="background:{badge_bg};color:{badge_fg};">{html.escape(str(p.get("status", "")))}</span>
        </div>
        """

    shortage_html = ""
    for s in shortage[:3]:
        shortage_html += f"""
        <div class="row-item">
          <div>
            <div class="item-title">{html.escape(str(s.get("spec_id", "")))}</div>
            <div class="item-sub">{html.escape(str(s.get("neighborhood_id", "")))} · {html.escape(str(s.get("adapter", "")))}</div>
          </div>
          <span class="pill">Shortage: {float(s.get("shortage_score", 0.0)):.1f}</span>
        </div>
        """

    ideas_html = ""
    for idea in ideas[:4]:
        ideas_html += f"""
        <div class="row-item">
          <div>
            <div class="item-title">{html.escape(str(idea.get("title", "")))}</div>
            <div class="item-sub">{html.escape(str(idea.get("category", "")))} · Status: {html.escape(str(idea.get("status", "")))}</div>
          </div>
          <span class="pill">⚖️ {float(idea.get("vote_weight", 0.0)):.2f} wt</span>
        </div>
        """

    bounties_html = ""
    for b in bounties[:3]:
        bounties_html += f"""
        <div class="row-item">
          <div>
            <div class="item-title">{html.escape(str(b.get("bounty_id", "")))}</div>
            <div class="item-sub">Gap: {html.escape(str(b.get("gap_domain", "")))} · Base: {html.escape(str(b.get("suggested_base", "")))}</div>
          </div>
          <span class="pill">🎯 +{float(b.get("reward_credits", 0.0)):.1f} cr ({html.escape(str(b.get("status", "")))})</span>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  .hub-wrap {{
    width: 780px;
    max-width: 100%;
    color: var(--foreground, #e2e8f0);
    font-size: 13px;
    line-height: 1.45;
    padding: 4px 0;
  }}
  .hub-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 14px;
    border: 1px solid var(--border, rgba(148,163,184,0.22));
    border-radius: 10px;
    background: var(--card, rgba(15,23,42,0.55));
    margin-bottom: 10px;
  }}
  .hub-title {{
    font-size: 15px;
    font-weight: 700;
    letter-spacing: -0.01em;
  }}
  .hub-sub {{
    font-size: 11.5px;
    color: var(--muted-foreground, #94a3b8);
    margin-top: 2px;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 10px;
  }}
  .kpi-card {{
    border: 1px solid var(--border, rgba(148,163,184,0.22));
    border-radius: 9px;
    background: var(--card, rgba(15,23,42,0.55));
    padding: 10px 12px;
  }}
  .kpi-label {{
    font-size: 11px;
    color: var(--muted-foreground, #94a3b8);
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .kpi-val {{
    font-size: 18px;
    font-weight: 700;
    margin-top: 3px;
    color: var(--foreground, #f8fafc);
  }}
  .kpi-note {{
    font-size: 11px;
    color: var(--muted-foreground, #94a3b8);
    margin-top: 2px;
  }}
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 10px;
  }}
  .panel {{
    border: 1px solid var(--border, rgba(148,163,184,0.22));
    border-radius: 10px;
    background: var(--card, rgba(15,23,42,0.55));
    padding: 12px 14px;
  }}
  .panel-title {{
    font-size: 12.5px;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .row-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid var(--border, rgba(148,163,184,0.12));
  }}
  .row-item:last-child {{
    border-bottom: none;
  }}
  .item-title {{
    font-weight: 500;
    font-size: 12.5px;
  }}
  .item-sub {{
    font-size: 11px;
    color: var(--muted-foreground, #94a3b8);
  }}
  .pill {{
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid var(--border, rgba(148,163,184,0.25));
    white-space: nowrap;
  }}
  .bar-bg {{
    width: 100%;
    height: 8px;
    border-radius: 999px;
    background: rgba(148,163,184,0.18);
    overflow: hidden;
    margin: 6px 0 4px 0;
  }}
  .bar-fill {{
    height: 100%;
    background: var(--accent, #38bdf8);
    border-radius: 999px;
  }}
  .btn-row {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 8px;
  }}
  .act-btn {{
    cursor: pointer;
    font-size: 11.5px;
    font-weight: 500;
    padding: 5px 10px;
    border-radius: 7px;
    border: 1px solid var(--border, rgba(148,163,184,0.3));
    background: transparent;
    color: var(--foreground, #f8fafc);
  }}
  .act-btn:hover {{
    border-color: var(--accent, #38bdf8);
  }}
</style>
</head>
<body>
<div class="hub-wrap">
  <div class="hub-header">
    <div>
      <div class="hub-title">🕸️ HACMDN-Net Contributor &amp; Node Operator Hub (v0.3.0)</div>
      <div class="hub-sub">Operator: <strong>{op_id}</strong> · Mode: {html.escape(str(wstate.get("compute_mode", "auto_game_guard")))} · Game-Guard: {html.escape(str(hw.get("game_guard_status", "")))}</div>
    </div>
    <span class="pill" style="border-color:#22c55e;color:#22c55e;">● Mesh Active</span>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Total Earnings</div>
      <div class="kpi-val">+{total_cr:.2f} cr</div>
      <div class="kpi-note">70/10/10/10 Shared-Entity Ledger</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Worker + Royalties</div>
      <div class="kpi-val">{worker_cr:.2f} / {royalty_cr:.2f}</div>
      <div class="kpi-note">Inference (70%) · Adapter Royalty (10%)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Community Dividend</div>
      <div class="kpi-val">+{div_cr:.2f} cr</div>
      <div class="kpi-note">Overflow Pool: {overflow_pool:.1f} cr</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Inference Contributed</div>
      <div class="kpi-val">{tasks_done} tasks</div>
      <div class="kpi-note">{tokens_done:,} verified tokens</div>
    </div>
  </div>

  <div class="panel" style="margin-bottom:10px;">
    <div class="panel-title">
      <span>🛡️ Anti-Whale Community Cap &amp; Datacenter Overflow Protection</span>
      <span class="item-sub">{worker_cr:.2f} / {daily_cap:.1f} cr daily personal cap ({cap_pct:.1f}%)</span>
    </div>
    <div class="bar-bg"><div class="bar-fill" style="width:{max(4.0, min(100.0, cap_pct))}%;"></div></div>
    <div class="item-sub">
      {html.escape(str(policy.get("split_formula", "")))} — {html.escape(str(policy.get("overflow_policy", "")))}
    </div>
    <div class="btn-row">
      <button class="act-btn" data-hermes-send="Use hacmdn_contributor_hub with action='simulate_datacenter_overflow' and raw_datacenter_credits=120.0, then refresh the hub preview widget">⚡ Simulate Datacenter Overflow (+120 cr)</button>
      <button class="act-btn" data-hermes-send="Use hacmdn_bounty_flywheel with action='run_idle_pool_task' and idle_pool_category='open-science', then refresh the hub preview widget">🧬 Run Idle Open-Science Task</button>
      <button class="act-btn" data-hermes-send="Use hacmdn_worker_pool with action='auto_load_needed_specialist', then refresh the hub preview widget">🔄 Auto-Load Most Needed Specialist</button>
    </div>
  </div>

  <div class="two-col">
    <div class="panel">
      <div class="panel-title">
        <span>⚙️ Subscribed Compute Pools</span>
        <span class="item-sub">{int(hw.get("cpu_threads", 16))} threads · {float(hw.get("available_ram_gb", 16.0)):.1f} GB RAM</span>
      </div>
      {pools_html}
    </div>
    <div class="panel">
      <div class="panel-title">
        <span>📡 Neighborhood Specialist Shortage Index</span>
        <span class="item-sub">Warm: {html.escape(str(wstate.get("active_loaded_specialist", "")))}</span>
      </div>
      {shortage_html}
    </div>
  </div>

  <div class="two-col">
    <div class="panel">
      <div class="panel-title">
        <span>💡 Ideas &amp; Directives Pitched to Community</span>
        <span class="item-sub">Stake-Weighted Votes</span>
      </div>
      {ideas_html}
    </div>
    <div class="panel">
      <div class="panel-title">
        <span>🎯 Open JIT Fine-Tuning Bounties</span>
        <span class="item-sub">Triggered by Abstentions</span>
      </div>
      {bounties_html}
    </div>
  </div>
</div>
</body>
</html>
"""


def write_hub_preview_html(
    snapshot: dict[str, Any],
    output_path: Optional[str | Path] = None,
) -> Path:
    """Write the Contributor Hub HTML widget to disk and return its absolute Path."""
    if output_path:
        path = Path(output_path)
    else:
        scratch_dir = Path.home() / ".hermes" / "cache" / "scratch"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        path = scratch_dir / "hacmdn-contributor-hub.html"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_hub_html(snapshot), encoding="utf-8")
    return path


def serve_local_gui(port: int = 8765) -> None:
    """Run a lightweight loopback HTTP server serving the live Contributor Hub on 127.0.0.1."""
    try:
        from .network import get_network
    except ImportError:
        from network import get_network  # type: ignore[no-redef]

    class HubHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            net = get_network()
            if self.path.startswith("/api/hub"):
                snap = net.manage_contributor_hub({"action": "get_hub_snapshot"})
                body = json.dumps(snap, indent=2).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            snap = net.manage_contributor_hub({"action": "get_hub_snapshot"})
            html_bytes = render_hub_html(snap).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

    server = HTTPServer(("127.0.0.1", port), HubHandler)
    print(f"HACMDN-Net Contributor Hub GUI listening on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
