## Summary

Adds **`hacmdn`** (**HACMDN-Net — Hermes Agent Community Microtuned Decentralized Network**, `v1.0.0`) to `plugin-catalog/hacmdn.yaml`, pinned to [`Jpalmer95/hacmdn-net@11ac5d7a22222e607900719ddd3f822b5c183f83`](https://github.com/Jpalmer95/hacmdn-net/commit/11ac5d7a22222e607900719ddd3f822b5c183f83).

Instead of routing every task to a monolithic frontier LLM or sharding one giant model across nodes, **HACMDN-Net** organizes a neighborhood mesh of **tiny, minimum-viable fine-tuned specialists** (`Qwen/Qwen3-0.6B` to `4B` Apache-2.0 base family) that:
1. **Excel at narrow contracts with calibrated brutal honesty:** Each `0.6B` LoRA specialist is trained on a strict input/output transformation plus an explicit conformal abstention boundary (`[ABSTAIN: OUT_OF_SCOPE]`). In our held-out pilot benchmark (`data/pilot_eval_results.json`), all 3 starting `Qwen/Qwen3-0.6B` LoRA specialists achieved **100% held-out accuracy** (vs `0%–30%` untouched base), **100% OOD abstention**, and **1.0000 ROC-AUC** while running on spare CPU threads alongside an active GPU workload.
2. **Route via Neighborhood Connectors, Confidence-Weighted Bidding & a 6-Tier Escalation Ladder:**
   - **Tier 0:** Local Micro-Specialist (`0.6B` LoRA)
   - **Tier 1:** Fine-tuned Neighborhood Connector (`jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1`) + Confidence-Weighted Direct & Proxy Bids
   - **Tier 2:** Organizer Super-Peer Cross-Neighborhood `kNN` Bridge
   - **Tier 3:** Hugging Face ZeroGPU Community Load-Balancing Buffer ([`jkorstad/hacmdn-community-buffer`](https://huggingface.co/spaces/jkorstad/hacmdn-community-buffer))
   - **Tier 4 / Tier 5:** Upstream Generalist Handoff (`NousResearch/Hermes-4-14B`) + Structured Network Abstention that automatically opens an escrowed **JIT Fine-Tuning Bounty**
3. **Close the loop with an Execution-Verified Synthetic Distillation Factory (`training/distill_specialist.py`):** Synthesizes candidate training pairs for recurring abstention gaps, filters every candidate through deterministic execution verifiers (in-memory `sqlite3` SQL/window execution, JSON-RPC 2.0 schema validation, Python AST contract inspection), mixes a **40% Hard-Negative + OOD Boundary Abstention DPO curriculum**, calibrates the conformal threshold ($\le 10\%$ wrong-accept risk), and enforces **Eval-Before-Gossip** (`eval_score >= base_model_score + 0.15`).
4. **Protect hobbyists with a 70/10/10/10 Shared-Entity Split, Anti-Whale Cap & L402 Lightning Settlement:**
   - **70% Worker / 10% Adapter Author Royalty / 10% Connector / 10% Shared Community Pool**
   - **50.0 cr/day Anti-Whale Personal Cap:** Compute donated above the daily personal cap by mega-clusters/datacenters overflows 100% into the **Philanthropic Community Dividend & Open-Science Pool**, enriching small contributors rather than diluting them.
   - **L402 Lightning Settlement:** Settles accumulated credits & cooperative dividends into cryptographic L402 macaroons (`HMAC-SHA256` caveats) + `SHA-256` preimage commitments and BOLT11 invoices.

---

## Hermes Surfaces Used

- **7 LLM Tools (`toolset="hacmdn"` via `ctx.register_tool`):**
  - `hacmdn_route_query`
  - `hacmdn_publish_specialist`
  - `hacmdn_bid_task`
  - `hacmdn_bounty_flywheel`
  - `hacmdn_network_status`
  - `hacmdn_worker_pool`
  - `hacmdn_contributor_hub`
- **In-Session Slash Command (`ctx.register_command`):** `/hacmdn [status|hub|pools|rendezvous|p2p|distill|l402|pitch|route|bid|bounties|vote|idle]`
- **CLI Subcommand (`ctx.register_cli_command`):** `hermes hacmdn <subcommand>`
- **Bundled Skill (`ctx.register_skill`):** `hacmdn-network` (`skills/hacmdn-network/SKILL.md`)
- **Hermes Desktop Native Plugin (`desktop/plugin.js`):** Built strictly with `@hermes/plugin-sdk` and `react/jsx-runtime` (`PANES_AREA` right-docked **HACMDN Hub** pane + `STATUSBAR_AREAS.right` telemetry chip).
- **Hermes Web Dashboard Extension (`dashboard/`):** `dashboard/manifest.json`, `dashboard/plugin_api.py` (`APIRouter` using `asyncio.to_thread`), and `dashboard/dist/index.js` (`window.__HERMES_PLUGIN_SDK__` IIFE).
- **Public Core Imports Only:** Uses `plugins.plugin_storage.plugin_db("hacmdn")` for profile-scoped SQLite storage and `agent.secret_scope.get_secret("HF_TOKEN")` for optional Hugging Face token access.

---

## Rule 13 Disclosure

- **Local Storage:** Stores neighborhood capability descriptors, fine-tuning bounties, work queues, P2P blob metadata, and attribution receipts in a profile-scoped SQLite database via `plugins.plugin_storage.plugin_db("hacmdn")` (`~/.hermes/plugin-data/hacmdn/data.db`). Writes HTML preview widgets and synthetic distillation curricula to `~/.hermes/cache/scratch/`.
- **System Reads:** Reads `/proc/meminfo` on Linux to inspect available RAM for Game-Guard hardware profiling (`network.py`).
- **Credentials:** Optional `HF_TOKEN` is declared as `type: secret` in `plugin.yaml` and read exclusively via `agent.secret_scope.get_secret("HF_TOKEN")`. No `.env` files, `auth.json`, keychains, or external credential stores are read.
- **Network / Local Servers:** Core routing, bidding, distillation verification, and ledger tools run deterministically against the local SQLite coordinator with zero unsolicited network egress. The dashboard extension mounts `/api/plugins/hacmdn/{hub,action,rendezvous}` inside the Hermes dashboard; `hermes hacmdn gui --serve` starts a loopback-only HTTP server on `127.0.0.1:8765` only when explicitly invoked by the user. No telemetry, no self-updating code, and no binary weights shipped in the plugin repository (verified LoRA adapters live on Hugging Face under [`jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network`](https://huggingface.co/collections/jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network-6aef78f6e0ea208136c602e5)).

---

## Screenshots

![HACMDN-Net Architecture Banner](https://raw.githubusercontent.com/Jpalmer95/hacmdn-net/11ac5d7a22222e607900719ddd3f822b5c183f83/docs/assets/banner.png)

![HACMDN-Net Contributor & Node Operator Hub](https://raw.githubusercontent.com/Jpalmer95/hacmdn-net/11ac5d7a22222e607900719ddd3f822b5c183f83/docs/assets/contributor-hub.png)

---

## Validation

- [x] `python3 scripts/validate_plugin_catalog.py plugin-catalog/hacmdn.yaml` → `OK: 1 file(s) valid`
- [x] `hermes plugins validate --install-deps` on clean clone at `11ac5d7a22222e607900719ddd3f822b5c183f83` → `Validation passed` (`✓ security scan — safe`, `✓ no core override`, `✓ desktop surface`)
- [x] `python3 scripts/scan_plugin_payloads.py` → `0` findings (clean source-only tree)
- [x] `hermes plugins doctor --ci` → `OK (7 tools registered)`
- [x] `pytest tests/` → `10 passed in 0.32s`
