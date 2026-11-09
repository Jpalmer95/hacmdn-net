# HACMDN-Net (`hacmdn`) — Hermes Agent Community Microtuned Decentralized Network Plugin

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![HF Collection](https://img.shields.io/badge/🤗_HF_Collection-HACMDN--Net-yellow)](https://huggingface.co/collections/jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network-6aef78f6e0ea208136c602e5)
[![ZeroGPU Space](https://img.shields.io/badge/🤗_ZeroGPU_Buffer-jkorstad%2Fhacmdn--community--buffer-indigo)](https://huggingface.co/spaces/jkorstad/hacmdn-community-buffer)

**HACMDN-Net** (**H**ermes **A**gent **C**ommunity **M**icrotuned **Decentralized** **N**etwork) is a native **Hermes Agent Plugin** (`hacmdn`) and decentralized specialist routing mesh. Instead of sending every subtask to a monolithic cloud LLM — or having 1,000 community nodes all run redundant copies of the same generalist base model — HACMDN-Net coordinates a diverse ecosystem of **laser-focused niche specialists across the entire consumer-grade spectrum (`10M` classifiers/translators $\rightarrow$ `0.6B–14B` micro-models $\rightarrow$ `32B` dense & sparse MoE models with small active parameters)** across modalities:

1. **Multi-Tier & Multi-Modal Specialization (`Millions of Params → 32B` & Sparse MoE):** Even a tiny classifier, parser, or translation model on a laptop CPU can execute an essential subtask inside a larger distributed workflow (`DeSci`, community R&D, or local business automation), while `8B–32B` and low-active-parameter MoE models on 8–24 GB consumer GPUs handle deep synthesis and orchestration.
2. **Topological Referral & Connector Routing + Calibrated Brutal Honesty:** Every model in the mesh is trained to know its exact boundary (`[ABSTAIN: OUT_OF_SCOPE]`) and **either knows the right specialist to refer a subtask to, OR knows a Neighborhood Connector (`Model #1`) or Organizer Super-Peer with richer topological contacts** up the 6-Tier Escalation Ladder to route the work across the community mesh.
3. **Value-Backed 70/10/10/10 Attribution & Community Fair-Share Cap (With Patron Compute Overflow):** All network earnings are **100% backed by the real value of verified work actually completed** (never unbacked inflation), split **70% Executing Worker / 10% Specialist Author Royalty / 10% Connector / 10% DeSci & Community Pool**. To preserve the earning capability of everyday low-compute contributors without dilution, personal daily rewards have a **Community Fair-Share Cap (`50.0 cr/day`)** — while any additional compute generously contributed by large clusters is welcomed as a **Patron Compute Overflow Grant** that funds open science and shared community dividends.
4. **ZeroGPU Buffer & Execution-Verified Distillation Factory:** Cold or unhosted niches fail over to the **Tier 3 Hugging Face ZeroGPU Community Buffer Space** ([`jkorstad/hacmdn-community-buffer`](https://huggingface.co/spaces/jkorstad/hacmdn-community-buffer)), while recurring abstention gaps trigger the **Autonomous Distillation Factory (`training/distill_specialist.py`)** using deterministic execution verifiers + 40% hard-negative boundary DPO.

---

## Live Hugging Face Ecosystem

- **🤗 Canonical Community Collection:** [`jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network-6aef78f6e0ea208136c602e5`](https://huggingface.co/collections/jkorstad/hacmdn-net-hermes-community-microtuned-specialist-network-6aef78f6e0ea208136c602e5)
- **🤗 Tier 3 ZeroGPU Community Buffer Space:** [`jkorstad/hacmdn-community-buffer`](https://huggingface.co/spaces/jkorstad/hacmdn-community-buffer)
- **🤗 Starting Verified Micro-Specialists (`Qwen/Qwen3-0.6B` LoRA):**
  1. **Model #1 (Neighborhood Connector & Triage Router):** [`jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1`](https://huggingface.co/jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1)
  2. **Model #2 (PostgreSQL 14+ CTE-to-Window Query Rewriter):** [`jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1`](https://huggingface.co/jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1)
  3. **Model #3 (Strict JSON-RPC 2.0 Tool-Call Synthesizer):** [`jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1`](https://huggingface.co/jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1)

---

## Verified Proof-of-Work Benchmark (§5 & §11 De-Risking Pilot)

Per §5 and §11 of the Feasibility Report and Architecture Spec v0.1, all three `Qwen/Qwen3-0.6B` LoRA micro-specialists were fine-tuned and evaluated against the untouched `Qwen/Qwen3-0.6B` base model on held-out in-domain and out-of-domain (OOD) test splits (`training/run_pilot_experiment.py`, full raw report in [`data/pilot_eval_results.json`](data/pilot_eval_results.json)):

| Specialist Model (`Qwen/Qwen3-0.6B` + LoRA `r=16`) | Untouched Base Score | Fine-Tuned Held-Out Score | In-Domain Accuracy | OOD Brutal-Honesty Abstention | Confidence Calibration ROC-AUC | §11 Verdict |
|---|---:|---:|---:|---:|---:|---|
| `qwen3-0.6b-neighborhood-connector-v1` | `30.00%` | **`100.00%`** (`+70.0%`) | **`100.00%`** (Base `0%`) | **`100.00%`** | **`1.0000`** | **PASS** |
| `qwen3-0.6b-sql-window-rewriter-v1` | `0.00%` | **`100.00%`** (`+100.0%`) | **`100.00%`** (Base `0%`) | **`100.00%`** | **`1.0000`** | **PASS** |
| `qwen3-0.6b-json-rpc-tool-caller-v1` | `0.00%` | **`100.00%`** (`+100.0%`) | **`100.00%`** (Base `0%`) | **`100.00%`** | **`1.0000`** | **PASS** |

All three §11 Pilot Acceptance Criteria passed:
- **Criterion 1 (`Specialist >= Base + 15%`):** Passed (`+70%` to `+100%` improvement over untouched `Qwen/Qwen3-0.6B`).
- **Criterion 2 (`Confidence Calibration ROC-AUC > 0.70`):** Passed (`AUC = 1.0000` across all 3 models; in-domain confidence `0.95–0.99` vs OOD task confidence `0.15–0.16`).
- **Criterion 3 (`End-to-End OOD Abstention >= 90% at <= 10% Wrong-Accept Risk`):** Passed (`100%` OOD abstention, `0%` wrong-accept risk).

---

## The 6-Tier Progressive Upstream Escalation Ladder

```
[Client Query]
      │
      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 0: Local Micro-Specialist (0.6B LoRA, ~95-135ms)                   │
│   └─ Direct domain match & Semantic-Entropy Confidence >= τ_abstain     │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ (Abstain / Not Local)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Neighborhood Connector + Confidence-Weighted Bidding Protocol   │
│   └─ Model #1 (`qwen3-0.6b-neighborhood-connector-v1`) triages domain   │
│   └─ Direct Worker Bids + Connector Proxy Bids (90% worker / 10% fee)   │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ (No Local Peer Above τ_abstain)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 2: Organizer Super-Peer Cross-Neighborhood Bridge (kNN Index)      │
│   └─ 2-hop gossip search across bridged neighborhood organizers         │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ (All P2P Workers Offline / TTL Expired)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 3: Hugging Face ZeroGPU Community Load-Balancing Buffer            │
│   └─ `jkorstad/hacmdn-community-buffer` dynamically serves approved     │
│      adapters from the HF Community Collection                          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ (No Verified Specialist Covers Domain)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Tier 4 & Tier 5: Upstream Generalist Handoff + JIT Fine-Tune Flywheel   │
│   └─ Tier 4: Escalates immediate completion to `Hermes-4-14B` / Host LLM│
│   └─ Tier 5: Emits structured `status: "abstain"` demand signal & opens │
│      an escrowed JIT Fine-Tuning Bounty in the neighborhood ledger      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Installation & Usage in Hermes Agent

### Install as a Hermes Plugin

```bash
# Clone directly into your Hermes plugins directory (or use hermes plugins install)
git clone https://github.com/Jpalmer95/hacmdn-net.git ~/.hermes/plugins/hacmdn

# Validate with Plugin Doctor & Catalog Validator
hermes plugins doctor ~/.hermes/plugins/hacmdn --ci
hermes plugins validate ~/.hermes/plugins/hacmdn

# Enable in Hermes
hermes plugins enable hacmdn
```

### LLM Tools Provided (`toolset: hacmdn`)

| Tool Name | Purpose |
|---|---|
| `hacmdn_route_query` | Route any query through the Neighborhood Connector, Bidding Protocol, and 6-Tier Escalation Ladder (with ZeroGPU Buffer fallback & escrow receipt). |
| `hacmdn_bid_task` | Run a transparent Confidence-Weighted Bidding round (direct worker bids + Neighborhood Connector proxy bids). |
| `hacmdn_publish_specialist` | Verify a new `Qwen3` specialist via **Eval-Before-Gossip** (`eval_score >= base_model_score + 0.15`) and publish its Capability Descriptor. |
| `hacmdn_bounty_flywheel` | List/open/claim/fulfill **JIT Fine-Tuning Bounties**, run the **Execution-Verified Synthetic Distillation Factory (`distill_bounty`)**, cast stake-weighted **Community Governance Votes**, or run **Idle Compute Pool** tasks (`open-science`, `local-business-aid`, `network-calibration`). |
| `hacmdn_network_status` | Inspect active neighborhoods, organizers, registered micro-specialists, ZeroGPU buffer status, and settled escrow receipts. |
| `hacmdn_worker_pool` | Profile hardware with **Game-Guard**, compute Shortage Scores, sync the **Outbound HTTPS/WSS Rendezvous Work-Queue & `llama.cpp` GGUF+LoRA Hot-Swap Daemon (`sync_rendezvous_daemon`)**, negotiate **Iroh QUIC P2P Hole-Punching & BLAKE3 LoRA Blob Gossip (`gossip_and_holepunch_p2p`)**, or execute parallel batch swarms. |
| `hacmdn_contributor_hub` | View **70/10/10/10 Shared-Entity Attribution** & **50.0 cr/day Anti-Whale Community Cap**, simulate philanthropic datacenter overflow, settle **L402 Lightning Network Micropayments & Cooperative Dividends (`settle_l402_and_dividends`, `verify_l402_receipt`)**, pitch community ideas, or export the Tri-Surface GUI Hub. |

### In-Session Slash Commands & CLI

```text
# Inside any Hermes chat session (CLI, Desktop, Telegram, Discord):
/hacmdn status
/hacmdn hub
/hacmdn pools
/hacmdn rendezvous
/hacmdn p2p
/hacmdn distill bounty-sqlite-to-duckdb-v1
/hacmdn l402
/hacmdn route Rewrite this PostgreSQL CTE query into a ROW_NUMBER() window function
/hacmdn bid Tool: create_invoice(customer_id='c9', amount=99)
/hacmdn bounties
/hacmdn vote open-science-antimalarial-docking
/hacmdn idle open-science

# From a terminal:
hermes hacmdn status
hermes hacmdn hub
hermes hacmdn pools
hermes hacmdn rendezvous
hermes hacmdn p2p
hermes hacmdn distill --bounty-id bounty-sqlite-to-duckdb-v1
hermes hacmdn l402
hermes hacmdn gui --serve
hermes hacmdn simulate
```

---

## Documentation & Architecture Thesis

- [`docs/thesis/01-concept-thesis.md`](docs/thesis/01-concept-thesis.md) — Original concept note: minimum-viable micro-specialists, brutal honesty, neighborhood connectors, bidding, and community governance.
- [`docs/thesis/02-feasibility-report-2026-11-07.md`](docs/thesis/02-feasibility-report-2026-11-07.md) — Layer-by-layer prior-art survey (Petals, exo, RouteLLM, MoA, Confidence-Driven Router, Voyager, mergekit) and risk analysis.
- [`docs/thesis/03-spec-v0.1.md`](docs/thesis/03-spec-v0.1.md) — Architecture Specification v0.1.
- [`docs/thesis/04-spec-v0.2-extensions.md`](docs/thesis/04-spec-v0.2-extensions.md) — v0.2 Extensions: Model #1 Neighborhood Connector, Confidence-Weighted & Proxy Bidding, 6-Tier Progressive Escalation Ladder, ZeroGPU Buffer, and Idle Compute Pool.
- [`docs/PILOT_PROOF_OF_WORK.md`](docs/PILOT_PROOF_OF_WORK.md) — Detailed walkthrough of the §5/§11 De-Risking Pilot Experiment and held-out evaluation outputs.

---

## License

Licensed under the **Apache License, Version 2.0** (`Copyright 2026 Jonathan Korstad`). See [`LICENSE`](LICENSE).
