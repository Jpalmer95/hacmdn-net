---
name: hacmdn-network
description: "Use when routing tasks across HACMDN-Net micro-specialists, publishing Capability Descriptors, bidding, or managing JIT fine-tuning bounties."
version: 1.0.0
author: Jonathan Korstad
license: Apache-2.0
---

# HACMDN-Net: Decentralized Micro-Specialist Network Workflow

Use the `hacmdn` plugin tools to route narrow tasks to tiny fine-tuned `Qwen/Qwen3-0.6B` specialists, evaluate semantic-entropy abstention, run confidence-weighted neighborhood bidding, execute autonomous execution-verified distillation, manage P2P mesh transport, or settle L402 Lightning micropayments.

## Core Tools

1. **`hacmdn_route_query`** — Route a query through the 6-Tier Progressive Upstream Escalation Ladder:
   - **Tier 0:** Local Micro-Specialist (`0.6B` LoRA)
   - **Tier 1:** Neighborhood Connector (`qwen3-0.6b-neighborhood-connector-v1`) + Peer Bid Winner
   - **Tier 2:** Neighborhood Organizer Super-Peer (`kNN` over capability descriptors)
   - **Tier 3:** Hugging Face ZeroGPU Community Buffer (`jkorstad/hacmdn-community-buffer`)
   - **Tier 4:** Upstream Generalist (`NousResearch/Hermes-4-14B` / active LLM)
   - **Tier 5:** Structured Network Abstention + Automatic JIT Fine-Tune Bounty Proposal

2. **`hacmdn_bid_task`** — Inspect all direct specialist bids and Neighborhood Connector proxy bids with calibrated confidence, semantic entropy, diversity penalty, and latency/cost weights.

3. **`hacmdn_publish_specialist`** — Register a new fine-tuned adapter after verifying **Principle 4** (approved `Qwen/Qwen3-0.6B` base family) and **Principle 5** (`Eval-Before-Gossip`: `eval_score >= base_model_score + 0.15`).

4. **`hacmdn_bounty_flywheel`** — Manage open fine-tuning bounties (`list_bounties`, `open_bounty`, `claim_bounty`, `submit_bounty_adapter`), run the **Execution-Verified Synthetic Distillation Factory** (`distill_bounty`), cast community governance votes (`vote_directive`), or donate spare cycles to the productive idle pool (`run_idle_pool_task` across `open-science`, `local-business-aid`, and `network-calibration`).

5. **`hacmdn_network_status`** — Inspect neighborhoods, organizers, registered micro-specialists, ZeroGPU buffer links, and escrowed settlement receipts.

6. **`hacmdn_worker_pool`** — Profile hardware with **Game-Guard**, compute Shortage Scores (`profile_and_recommend`, `auto_load_needed_specialist`), sync the **Outbound HTTPS/WSS Rendezvous Work-Queue & `llama.cpp` GGUF+LoRA Hot-Swap Daemon** (`sync_rendezvous_daemon`), negotiate **Iroh QUIC P2P Hole-Punching & BLAKE3 LoRA Blob Gossip** (`gossip_and_holepunch_p2p`), or execute parallel batch swarms (`run_parallel_batch`).

7. **`hacmdn_contributor_hub`** — Inspect the **70/10/10/10 Shared-Entity Attribution Ledger** and **50.0 cr/day Anti-Whale Community Cap**, simulate philanthropic datacenter overflow (`simulate_datacenter_overflow`), settle **L402 Lightning Network Micropayments & Cooperative Dividends** (`settle_l402_and_dividends`, `verify_l402_receipt`), pitch community ideas (`pitch_idea`), or export the interactive GUI Hub widget (`export_gui_widget`).
