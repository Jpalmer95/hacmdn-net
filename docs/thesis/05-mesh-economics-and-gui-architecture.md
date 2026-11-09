# HACMDN-Net Specification v0.3: Global Compute Mesh, High-Efficacy Distillation, Anti-Whale Economics & Optional GUI Hub

**Codename:** `HACMDN-Net`  
**Date:** 2026-11-07  
**Author:** Jonathan Korstad (`Jpalmer95` / `jkorstad`)

---

## 1. Global Decentralized Compute Mesh & Multi-Pool Work Allocation

To allow anyone, anywhere to install `hacmdn` and immediately contribute spare compute without port-forwarding or enterprise networking:

### 1.1 Two-Stage Networking Architecture (Outbound Rendezvous $\rightarrow$ Iroh/Hivemind P2P)
1. **Stage A — Outbound-Only Rendezvous & Buffer Coordinator (Zero Firewall Config):**
   - Home contributors are nearly always behind residential NAT or CGNAT.
   - Worker nodes establish an outbound HTTPS/WSS lease to Neighborhood Organizers and the **Hugging Face ZeroGPU Buffer Space** (`jkorstad/hacmdn-community-buffer`).
   - Nodes publish signed heartbeats (`ed25519` public key, loaded `spec_id` adapters, hardware tier, free RAM/VRAM, p95 latency) and long-poll or stream tasks from their subscribed work pools.
2. **Stage B — Iroh QUIC / libp2p Kademlia Direct Mesh:**
   - Once two nodes discover each other via an Organizer or DHT, **Iroh** (`n0-computer/iroh` QUIC hole-punching + DERP-style relay fallback) upgrades the connection to a direct peer-to-peer encrypted stream and gossips `~20 MB` LoRA `.safetensors` / `.gguf` adapters via content-addressed BLAKE3 hashes.

### 1.2 Four Concurrent Work Pools (Matching Problems to Model Type & Size)
When multiple tasks or complex decomposable problems hit the network simultaneously, Organizers allocate work across **four specialized pools**:

| Pool ID | Name | Target Hardware & Model Size | Allocation Strategy |
|---|---|---|---|
| `pool-interactive-micro` | **Real-Time Micro-Inference** | `0.6B` LoRA warm in RAM/VRAM (`<150ms` p95) | Confidence-weighted bidding winner; single-hop execution. |
| `pool-parallel-batch` | **Map-Reduce Sub-Problem Swarm** | `N × 0.6B–1.7B` concurrent workers | Decomposes multi-item jobs (e.g. 50 SQL migrations or 100 schema syntheses) across $N$ community nodes in parallel and merges verified outputs. |
| `pool-idle-community` | **Open-Science, Local-Business & Calibration** | Spare CPU threads / idle GPU (`0.6B Q4_K_M`) | Drained whenever a node is opted-in and no paid interactive query is queued; includes `5%` sampling audits and conformal calibration probes. |
| `pool-jit-finetune` | **Autonomous Specialist Training & Eval** | `>= 8 GB` VRAM or `>= 16` CPU threads | Claims open abstention bounties, runs LoRA distillation, and executes canonical `Eval-Before-Gossip` holdout benchmarks. |

### 1.3 Hardware & "Game-Guard" Profiler + Shortage-Driven Auto-Loader
- **Game-Guard / Primary-Workload Protection:** Before claiming a task or loading an adapter, the local worker checks GPU VRAM and utilization (`nvidia-smi` / `torch.cuda.mem_get_info`). If a game (e.g. *Cyberpunk 2077*), 3D renderer (*Blender*), or local LLM is using the GPU, the worker automatically shifts to **Spare-CPU Micro Mode** (`0.6B` on capped CPU threads) or pauses GPU claims so the user never experiences frame drops.
- **Shortage-Driven Model Selection:** Rather than every contributor running the same popular model, nodes query the neighborhood's **Shortage Index**:
  $$\text{ShortageScore}(s) = \frac{\text{RecentRequests}(s) + 2 \cdot \text{AbstentionNearMisses}(s) + 3 \cdot \text{ZeroGPUBufferHits}(s)}{\max(1, \text{OnlineWorkers}(s))}$$
  and preload the approved `Qwen/Qwen3-0.6B` adapter with the highest shortage score that fits their RAM/VRAM budget.

---

## 2. High-Efficacy Micro-Model Training Factory

Why do `0.6B` models fail when used as generalists, yet achieve **100% held-out accuracy and 1.000 ROC-AUC** in our pilot? Because a micro-model has enough capacity to master **one strict transformation + its exact abstention boundary**, provided it is not forced to memorize world trivia.

The **HACMDN-Net Distillation Factory** (`training/`) standardizes four steps for every community niche model:
1. **Strict Contract Definition:** Every specialist defines a narrow `input_schema`, `output_schema`, and deterministic validation function (e.g. SQL parser/executor, JSON Schema / AST checker, regex/unit verifier).
2. **Execution-Verified Teacher Synthesis:** A frontier/generalist teacher generates diverse in-domain examples; only examples that pass the deterministic verifier enter the training split.
3. **Hard-Negative Boundary & OOD Curriculum (`40%` of training mix):**
   - `20%` **Hard Negatives** (adjacent tasks in the same surface language that belong to a *different* specialist, e.g., SQL DDL `ALTER TABLE` given to a SQL Window-Function specialist).
   - `20%` **General OOD Prompts** (creative writing, biology, finance, casual chat).
   - Both map strictly to `[ABSTAIN: OUT_OF_SCOPE] <reason>`.
4. **Full-Batch Balanced Gradient Accumulation + Conformal Calibration:** Every optimizer step averages gradients across balanced in-domain and OOD mini-batches so the adapter never oscillates toward always-answering or always-abstaining, followed by ROC-AUC conformal threshold fitting on the held-out split.

---

## 3. Attribution, Shared-Entity Payouts & The Anti-Whale / Anti-Datacenter Cap

### 3.1 The 70 / 10 / 10 / 10 Shared-Entity Attribution Split
Every settled task receipt (`escrow_credits`) is attributed across four roles:
- **70% $\rightarrow$ Executing Worker Node:** Rewards the contributor whose hardware ran the inference.
- **10% $\rightarrow$ Specialist Adapter Author Royalty:** Ongoing passive attribution to the contributor who fine-tuned and published the winning `Qwen3` LoRA adapter!
- **10% $\rightarrow$ Neighborhood Connector / Organizer Super-Peer:** Rewards topological indexing, proxy bidding, and conformal calibration probing.
- **10% $\rightarrow$ Shared Community Treasury & Idle Pool:** Funds `open-science`, `local-business-aid`, and new `JIT Fine-Tuning Bounties`.

### 3.2 Anti-Whale Concave Curve & Datacenter Overflow Grant
To prevent a mega-cluster or commercial datacenter from joining with 1,000 GPUs and diluting community payouts:
1. **Sub-Linear Scaling & Daily Personal Cap ($\text{CAP}_{\text{daily}} = 50.0\text{ credits/day}$ per operator identity):**
   $$\text{PersonalPayout}(u) = \min\Big(\text{CAP}_{\text{daily}},\; \text{RawEarned}(u)^{0.85} \cdot \text{ScarcityBonus}\Big)$$
2. **Philanthropic Datacenter Overflow:**
   - Any compute contributed beyond $\text{CAP}_{\text{daily}}$ is **not rejected** — the network welcomes the donated capacity!
   - Instead, 100% of the credits earned above $\text{CAP}_{\text{daily}}$ are automatically routed into the **Community Dividend & Open-Science Overflow Pool**, which is redistributed *pro-rata* to verified small community nodes (`<= 2` GPUs / CPU workers) and open-science bounties.
   - The large donor receives verifiable **Community Patron / Open-Science Philanthropist** attribution on the public ledger without ever crowding out hobbyist earnings.

---

## 4. Optional Lightweight GUI Hub Architecture

The `hacmdn` plugin ships an optional, zero-bloat GUI across three surfaces:
1. **Hermes Desktop Native Pane & Status-Bar Chip (`desktop/plugin.js`):**
   - Built on `@hermes/plugin-sdk` (`react/jsx-runtime`, zero build step).
   - Adds a status-bar telemetry chip (`🕸️ HACMDN`) and a dockable **HACMDN Node Hub** pane calling `/api/plugins/hacmdn/hub`.
2. **Hermes Web Dashboard Tab (`dashboard/manifest.json` + `dashboard/plugin_api.py` + `dashboard/dist/index.js`):**
   - Adds a **HACMDN-Net** tab to `hermes dashboard` (`http://127.0.0.1:9119/hacmdn`).
3. **Standalone Local Web Hub (`hermes hacmdn gui`) & Inline Chat Widget (`::preview`):**
   - Launches a lightweight local web server (`127.0.0.1:8765`) or renders an interactive HTML widget directly inside Hermes Desktop chat showing:
     - **My Node & Game-Guard Status:** Active compute mode (`Spare CPU` vs `GPU`), loaded specialists, Shortage Score auto-selection, and work-pool toggles.
     - **Earnings & Anti-Whale Attribution Meter:** Personal credits earned, Adapter Author Royalties, Community Cap progress bar (`X / 50.0 cr/day`), and Datacenter Overflow Pool dividends.
     - **Community Ideas, Bounties & Governance Pitches:** Pitch a new community directive or niche model idea, vote with stake+reputation weight, and inspect live task receipts.
