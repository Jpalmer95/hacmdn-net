# HACMDN-Net — Master Plan

**Project:** Hermes Agent Community Microtuned Decentralized Network (`hacmdn-net`)  
**Repository:** `https://github.com/Jpalmer95/hacmdn-net`  
**Hugging Face Ecosystem:** `jkorstad` (Models, ZeroGPU Buffer Space, Community Collection)  
**License:** Apache-2.0 (`Copyright 2026 Jonathan Korstad`)

---

## Vision & Core Thesis

A decentralized neighborhood of tiny, minimum-viable fine-tuned specialist models (`Qwen/Qwen3-0.6B` Apache-2.0 base family) with **calibrated brutal honesty (abstention)**, interconnected through **Neighborhood Connectors** and **Organizer Super-Peers**, that bids on tasks, routes progressively upstream when out-of-scope, uses **Hugging Face ZeroGPU Spaces** as a cold-start load-balancing buffer, and turns recurring abstentions into a **JIT fine-tuning flywheel**.

---

## Recorded Architectural Decisions

1. **Single Base Family (`Qwen/Qwen3-0.6B`, Apache-2.0):** Standardized so all community LoRA specialists share a compatible weight space for `mergekit` (DARE/TIES) "neighborhood soup" merges and rapid adapter hot-swapping on a single 12 GB GPU or ZeroGPU Space.
2. **Brutal Honesty as a First-Class Protocol Primitive:** Every specialist is trained on both positive domain examples and explicit out-of-domain abstention examples (`[ABSTAIN: OUT_OF_SCOPE]`), combined with semantic-entropy / token-confidence conformal calibration (`arXiv:2502.11021`, `arXiv:2502.06884`).
3. **Neighborhood Connector + Confidence-Weighted Bidding:** Rather than a monolithic central router, Model #1 (`qwen3-0.6b-neighborhood-connector-v1`) knows the heads of niche groupings and coordinates a bidding protocol where specialists (or connectors bidding on behalf of downstream micro-models) compete on `Confidence * EvalMargin * Diversity / (Latency * Cost)`.
4. **6-Tier Progressive Upstream Escalation:** `Tier 0 (Local Micro-Specialist)` → `Tier 1 (Neighborhood Connector + Peer Bid Winner)` → `Tier 2 (Organizer Super-Peer Cross-Neighborhood kNN)` → `Tier 3 (HF ZeroGPU Community Buffer)` → `Tier 4 (Upstream Generalist / Frontier)` → `Tier 5 (Network Abstention + JIT Bounty Proposal)`.
5. **Eval-Before-Gossip (`Verified-on-Entry`):** No capability descriptor enters neighborhood gossip unless its canonical eval score beats the untouched `Qwen/Qwen3-0.6B` base model by at least the domain margin (`+0.15`).
6. **ZeroGPU Community Buffer + HF Collection:** Solves early-network P2P churn by mirroring approved community specialists in a Hugging Face Collection and serving cold/unhosted niches via a Gradio 6 ZeroGPU Space (`jkorstad/hacmdn-community-buffer`).

---

## Roadmap & Milestones

### Phase 1: Thesis, Spec & Repository Foundation
- [x] Archive original thesis (`01-concept-thesis.md`), feasibility report (`02-feasibility-report-2026-11-07.md`), and Spec v0.1 (`03-spec-v0.1.md`).
- [x] Author Spec v0.2 Extensions (`04-spec-v0.2-extensions.md`): Neighborhood Connector, Bidding Protocol, 6-Tier Progressive Escalation, ZeroGPU Buffer, and Governance/Idle Pool.
- [x] Initialize Apache-2.0 license (`Copyright 2026 Jonathan Korstad`), `MASTER_PLAN.md`, and `AGENTS.md`.

### Phase 2: Hermes Agent Plugin (`hacmdn`)
- [x] Native Manifest v2 (`plugin.yaml`) + `register(ctx)` entrypoint (`__init__.py`).
- [x] Core Decentralized Network Engine (`network.py`) backed by profile-scoped SQLite (`plugins.plugin_storage.plugin_db("hacmdn")`):
  - Capability Descriptor Registry with TTL expiration & diversity fingerprint penalty
  - Confidence-Weighted Bidding & Downstream Proxy Bidding (`bid_on_task`)
  - Semantic-Entropy Confidence & Conformal Abstention Evaluator
  - 6-Tier Progressive Upstream Escalation Router (`route_query`)
  - Eval-Before-Gossip (`verify_and_publish_descriptor`)
  - JIT Fine-Tuning Bounty Flywheel + Community Governance Votes + Idle Open-Science/Local-Business Pool
  - Escrowed Per-Task Settlement + 5% Sampling Audits + 24h Challenge Slashing
- [x] 5 LLM Tools (`schemas.py`, `tools.py`):
  - `hacmdn_route_query`
  - `hacmdn_publish_specialist`
  - `hacmdn_bid_task`
  - `hacmdn_bounty_flywheel`
  - `hacmdn_network_status`
- [x] In-Session Slash Command (`/hacmdn`) & CLI Subcommand (`hermes hacmdn ...`).
- [x] Bundled Skill (`skills/hacmdn-network/SKILL.md`).
- [x] Pass `hermes plugins doctor`, `hermes plugins validate`, and `pytest` suite.

### Phase 3: De-Risking Pilot — Fine-Tuning 3 Real `Qwen/Qwen3-0.6B` Micro-Models on RTX 4070 Ti
- [x] Fine-tune **Model #1**: `jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1` (Neighborhood Connector, domain triage, downstream proxy bidder, OOD abstainer).
- [x] Fine-tune **Model #2**: `jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1` (PostgreSQL 14+ CTE-to-Window query rewriter + brutal-honesty OOD abstainer).
- [x] Fine-tune **Model #3**: `jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1` (Strict JSON-RPC / micro-function synthesizer + brutal-honesty OOD abstainer).
- [x] Execute §5/§11 Pilot Acceptance Benchmark (`training/run_pilot_experiment.py`) and record verified metrics in `data/pilot_eval_results.json` and `docs/PILOT_PROOF_OF_WORK.md`.

### Phase 4: Hugging Face Community Collection & ZeroGPU Buffer Space
- [x] Upload all 3 fine-tuned LoRA adapters + Capability Descriptors + Eval Reports to Hugging Face (`jkorstad/hacmdn-qwen3-0.6b-*`).
- [x] Build, verify, and deploy the Gradio 6 ZeroGPU Space `jkorstad/hacmdn-community-buffer`.
- [x] Create and populate the Hugging Face Collection unifying the models and Space.

### Phase 5: Public GitHub Release & Local Hermes Enablement
- [x] Publish `https://github.com/Jpalmer95/hacmdn-net`.
- [x] Install and enable `hacmdn` in `~/.hermes/plugins/hacmdn`.
