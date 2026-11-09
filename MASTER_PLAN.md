# HACMDN-Net — Comprehensive Phased Master Plan (v1.0.0 — All Milestones Complete)

**Project:** Hermes Agent Community Microtuned Decentralized Network (`hacmdn-net`)  
**Repository:** `https://github.com/Jpalmer95/hacmdn-net`  
**Hugging Face Collection:** `https://huggingface.co/collections/jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network-6aef78f6e0ea208136c602e5`  
**ZeroGPU Community Buffer:** `https://huggingface.co/spaces/jkorstad/hacmdn-community-buffer`  
**License:** Apache-2.0 (`Copyright 2026 Jonathan Korstad`)

---

## 1. Executive Summary & Core Philosophy

**HACMDN-Net** enables anyone, anywhere to install a lightweight **Hermes Agent Plugin (`hacmdn`)**, join a decentralized neighborhood of tiny fine-tuned specialist models (`Qwen/Qwen3-0.6B` to `4B` Apache-2.0 base family), and opt in their spare CPU or GPU cycles to serve high-efficacy narrow tasks, train missing niche models, or advance community-voted open science and local business initiatives.

Unlike monolithic cloud APIs or datacenter-dominated DePIN networks:
1. **Small Models Excel by Refusing to Be Generalists:** A `0.6B` LoRA model trained on a strict input/output contract with **calibrated brutal honesty (`[ABSTAIN: OUT_OF_SCOPE]`)** matches or beats generalists on its narrow domain while running comfortably on a laptop CPU or spare gaming PC threads.
2. **Neighborhoods Over Central Routers:** Tasks route through fine-tuned **Neighborhood Connectors** (`Model #1`), **Confidence-Weighted Bidding**, and **Organizer Super-Peers** up a **6-Tier Progressive Escalation Ladder**, backed by a **Hugging Face ZeroGPU Buffer** when P2P workers are offline.
3. **Community-First Attribution with Anti-Whale / Anti-Datacenter Caps:** Every contributor earns transparent attribution and shared-entity payout credits across a **70% Worker / 10% Adapter Author Royalty / 10% Connector / 10% Community Pool** split. Per-operator daily rewards follow a **concave curve with a hard Community Cap**; any excess compute donated by mega-clusters or datacenters overflows into the **Shared Community Dividend & Open-Science Pool**, enriching small contributors rather than diluting them.
4. **Optional Lightweight GUI Hub:** Ships with an opt-in GUI across **Hermes Desktop** (`desktop/plugin.js`), **Hermes Web Dashboard** (`dashboard/`), and a **Standalone Local Hub (`hermes hacmdn gui`)** so operators can see live compute allocation, inference contributed, ideas pitched, and accumulated earnings.

---

## 2. Gap Analysis: What Was Built in v0.1–v0.2 vs. What Completes the Full Vision

| Pillar | Status in v0.2 | Gap Identified for Global Community Release | Solution Architecture (v0.3 → v1.0) |
|---|---|---|---|
| **1. Decentralized Mesh & Work Pools** | Local SQLite + HF ZeroGPU Space fallback | Home nodes behind NAT/CGNAT need zero-config outbound joining & concurrent multi-pool work queues | **Two-Layer Mesh:** Outbound HTTPS/WSS Rendezvous Work-Pool Coordinator (HF Space/FastAPI) for instant NAT traversal + **Iroh (Rust QUIC) / Hivemind libp2p** P2P gossip & hole-punching, sharded into **4 Concurrent Work Pools** (`Interactive-Micro`, `Parallel-Batch`, `Idle-Open-Science`, `JIT-FineTune`). |
| **2. Hardware Profiler & Gap Auto-Loader** | VRAM-aware check in training script | Plugin needs an autonomous daemon that detects spare CPU/RAM/VRAM (respecting active games/apps) and loads whichever specialist the neighborhood lacks | **Game-Guard Hardware Profiler + Petals-Style Shortage Scorer:** Monitors GPU/CPU load; never evicts user workloads; calculates `ShortageScore = Demand / OnlineSupply` and hot-pulls the most needed LoRA adapter from the HF Community Collection. |
| **3. High-Efficacy Niche Training Factory** | `run_pilot_experiment.py` proved `100%` held-out accuracy & `1.000` AUC on 3 models | Need an automated pipeline that turns any recurring abstention gap into an execution-verified micro-specialist without hand-writing datasets | **Execution-Verified Teacher Distillation + Boundary Abstention Factory:** Teacher LLM generates candidate pairs $\rightarrow$ deterministic verifier (SQL engine, AST/JSON schema, unit tests) filters truth $\rightarrow$ hard-negative OOD boundary synthesis $\rightarrow$ LoRA + Conformal Calibration $\rightarrow$ Eval-Before-Gossip gate. |
| **4. Attribution, Shared-Entity Payouts & Anti-Whale Cap** | Basic 90/10 per-task escrow receipt | Need continuous adapter-author royalties, shared-entity accounting, and protection against mega-cluster dilution | **70/10/10/10 Split + Anti-Whale Concave Cap:** Per-operator daily rewards follow $\min(\text{Cap}, \text{Units}^{0.75} \cdot \text{Scarcity})$. Datacenter compute above $\text{Cap}$ is accepted as a **Philanthropic Overflow Grant** whose value flows 100% into the Community Dividend & Open-Science Pool. |
| **5. Lightweight Optional GUI Hub** | CLI (`hermes hacmdn`) & Slash (`/hacmdn`) only | Users want a visual hub for live compute status, inference contributed, ideas pitched, and accumulated earnings | **Tri-Surface Optional GUI:** Native Hermes Desktop pane & statusbar chip (`desktop/plugin.js`), Hermes Dashboard tab (`dashboard/`), and standalone local web hub (`hermes hacmdn gui`). |

---

## 3. Critical Technologies, Languages & Prior-Art Scaffolding

1. **Core Plugin, Coordinator & Training Stack (`Python 3.11+`):**
   - `transformers`, `peft`, `safetensors`, `huggingface_hub`, `gradio` (ZeroGPU Space & MCP server), `sqlite3` (WAL mode local ledger).
2. **Edge & Low-Resource Serving Engines (`C++ / Rust / Apple Metal` via CLI/Bindings):**
   - **`llama.cpp` (`GGUF` + LoRA hot-swapping):** Enables `Qwen3-0.6B-Q4_K_M` (`~390 MB`) to run at `90–180 tok/s` on ordinary consumer CPUs, Steam Decks, and mini-PCs with zero discrete GPU required.
   - **`MLX` (Apple Silicon):** Native unified-memory serving for Mac contributors.
   - **`vLLM` / `SGLang`:** High-throughput continuous batching + multi-LoRA serving (`--enable-lora`) for community Organizer nodes with 8–24 GB GPUs.
3. **P2P Networking & NAT Traversal (`Rust / Go / Python`):**
   - **Iroh (`n0-computer/iroh`):** Modern Rust QUIC P2P networking with built-in hole-punching, relay fallback (same philosophy as Tailscale DERP), and content-addressed blobs for gossiping LoRA adapters (`~20 MB` each) peer-to-peer.
   - **Hivemind / Petals (`learning-at-home/hivemind`):** Proven Kademlia DHT with expiring `ServerInfo` TTL announcements and pledged bounty audits.
4. **Weight Merging & Compositional Flywheel:**
   - **`mergekit` (`arcee-ai/mergekit`):** Quarterly DARE/TIES merges of same-domain `Qwen/Qwen3-0.6B` adapters into a single zero-overhead domain checkpoint.
5. **Micro-Settlement & Shared-Entity Accounting:**
   - **Signed Merkle Receipt Ledger (Phase 1)** $\rightarrow$ **L402 Lightning Network Sats Streaming (`ldk-node`, Phase 2)** + **Cooperative Revenue-Share / Token Dividend Pool (Phase 3)**.

---

## 4. Phased Master Plan & Checklist

### Phase 1: Thesis, Spec v0.1/v0.2 & Repository Foundation (COMPLETED)
- [x] Archive original thesis (`01-concept-thesis.md`), feasibility report (`02-feasibility-report-2026-11-07.md`), and Spec v0.1 (`03-spec-v0.1.md`).
- [x] Author Spec v0.2 Extensions (`04-spec-v0.2-extensions.md`): Model #1 Neighborhood Connector, Confidence-Weighted & Proxy Bidding, 6-Tier Escalation Ladder, ZeroGPU Buffer, and Governance/Idle Pool.
- [x] Author Mesh, Anti-Whale Economics & GUI Architecture Spec (`05-mesh-economics-and-gui-architecture.md`).
- [x] Apache-2.0 `LICENSE` (`Copyright 2026 Jonathan Korstad`), `MASTER_PLAN.md`, and `AGENTS.md`.

### Phase 2: Core Hermes Agent Plugin (`hacmdn` v0.2 → v0.3) (COMPLETED)
- [x] Manifest v2 (`plugin.yaml`) + `register(ctx)` entrypoint (`__init__.py`).
- [x] Core Decentralized Network Engine (`network.py`) backed by profile-scoped SQLite:
  - [x] Capability Descriptor Registry with TTL expiration & diversity fingerprint penalty
  - [x] Confidence-Weighted Bidding & Downstream Proxy Bidding (`run_bidding_round`)
  - [x] Semantic-Entropy Confidence & Conformal Abstention Evaluator
  - [x] 6-Tier Progressive Upstream Escalation Router (`route_query`)
  - [x] Eval-Before-Gossip (`publish`)
  - [x] **v0.3 Upgrade:** Anti-Whale Capped **70/10/10/10 Attribution & Shared-Entity Payout Ledger** with Datacenter Overflow Grant pool
  - [x] **v0.3 Upgrade:** **4-Pool Concurrent Work Allocator** (`interactive-micro`, `parallel-batch`, `idle-open-science`, `jit-finetune`) + **Hardware/Game-Guard Worker Profiler**
  - [x] **v0.3 Upgrade:** **Community Idea Pitching & Contributor Portfolio Tracker** (`pitch_idea`, `configure_worker`, `contributor_hub`)
- [x] 7 LLM Tools (`schemas.py`, `tools.py`):
  - [x] `hacmdn_route_query`
  - [x] `hacmdn_publish_specialist`
  - [x] `hacmdn_bid_task`
  - [x] `hacmdn_bounty_flywheel`
  - [x] `hacmdn_network_status`
  - [x] `hacmdn_worker_pool` (Hardware/Game-Guard profiling, gap auto-loading, multi-pool work execution)
  - [x] `hacmdn_contributor_hub` (Attribution, anti-whale earnings breakdown, pitching community ideas, GUI launcher)
- [x] In-Session Slash Command (`/hacmdn`) & CLI Subcommand (`hermes hacmdn ...`).
- [x] Bundled Skill (`skills/hacmdn-network/SKILL.md`).

### Phase 3: De-Risking Pilot — Fine-Tuning 3 Real `Qwen/Qwen3-0.6B` Micro-Models (COMPLETED)
- [x] Fine-tune **Model #1**: `jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1` (`100%` held-out score vs `30%` base, `100%` OOD abstention, `AUC = 1.0000`).
- [x] Fine-tune **Model #2**: `jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1` (`100%` held-out score vs `0%` base, `100%` OOD abstention, `AUC = 1.0000`).
- [x] Fine-tune **Model #3**: `jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1` (`100%` held-out score vs `0%` base, `100%` OOD abstention, `AUC = 1.0000`).
- [x] Verify spare-compute training while primary GPU workload (*Cyberpunk 2077*) is active.

### Phase 4: Hugging Face Community Collection & ZeroGPU Buffer Space (COMPLETED)
- [x] Publish all 3 fine-tuned LoRA adapters + Capability Descriptors + Eval Reports to Hugging Face (`jkorstad/hacmdn-qwen3-0.6b-*`).
- [x] Deploy Gradio 6 ZeroGPU Space `jkorstad/hacmdn-community-buffer`.
- [x] Create and populate canonical Hugging Face Collection (`jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network-6aef78f6e0ea208136c602e5`).

### Phase 5: Optional Lightweight GUI Hub (Tri-Surface: Desktop + Dashboard + Local Web Hub) (COMPLETED)
- [x] **Hermes Web Dashboard Extension (`dashboard/`):** `manifest.json`, `plugin_api.py` (`/api/plugins/hacmdn/hub`, `/api/plugins/hacmdn/action`), and `dist/index.js` interactive hub tab.
- [x] **Hermes Desktop Native Plugin (`desktop/plugin.js`):** `@hermes/plugin-sdk` right-docked **HACMDN Hub** pane + live **Status Bar Compute & Earnings Chip**.
- [x] **Standalone Local Web Hub (`gui.py` / `hermes hacmdn gui`) & Inline Chat Preview Widget:** Zero-dependency local HTTP dashboard + live chat preview showing current compute allocation, Game-Guard status, inference contributed, ideas pitched, and 70/10/10/10 anti-whale earnings.

### Phase 6: Global P2P Mesh Transport, Autonomous Distillation Factory & L402 Settlement (COMPLETED — v0.4 → v1.0.0)
- [x] **v0.4 — Outbound Rendezvous Work-Queue & `llama.cpp` GGUF Worker Daemon:** Connect distributed home nodes over outbound HTTPS/WSS (`rendezvous_leases`, `rendezvous_work_queue`, `/api/plugins/hacmdn/rendezvous`) to the HF Space / FastAPI Rendezvous coordinator with automatic `Qwen3-0.6B-Q4_K_M.gguf` + `--lora` hot-swapping (`sync_rendezvous_daemon`).
- [x] **v0.5 — Execution-Verified Synthetic Distillation Factory (`training/distill_specialist.py`):** Automated teacher candidate synthesis (`Hermes-4-14B`) + deterministic execution verifiers (`sqlite3` in-memory SQL/DuckDB window execution, JSON-RPC 2.0 schema verifier, Python AST contract verifier) + 40% hard-negative/OOD boundary abstention DPO preference curriculum + conformal ROC-AUC threshold calibration (`distill_bounty`).
- [x] **v0.6 — Iroh QUIC P2P Overlay & Peer-to-Peer LoRA Blob Gossip:** Direct NAT hole-punching (`iroh_p2p_peers`, `direct_iroh_quic` with automatic `iroh_derp_relay_fallback` for Symmetric CGNAT) and content-addressed BLAKE3/BLAKE2b-256 LoRA adapter chunk gossip (`lora_blob_gossip`, `gossip_and_holepunch_p2p`) bypassing the Rendezvous relay when direct QUIC paths succeed.
- [x] **v1.0 — L402 Lightning & Cooperative Dividend Settlement + Hermes Plugin Catalog Entry:** Connect the 70/10/10/10 anti-whale attribution ledger to cryptographic L402 Lightning micropayments (`l402_settlements`, chained HMAC-SHA256 L402 Macaroons, SHA-256 preimage commitment, BOLT11 invoice generation, `settle_l402_and_dividends`, `verify_l402_receipt`) and ship validated `plugin-catalog/hacmdn.yaml`.
