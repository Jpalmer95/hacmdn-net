# HACMDN-Net Specification v0.2 Extensions
**Codename:** `HACMDN-Net` (*Hermes Agent Community Microtuned Decentralized Network*)  
**Date:** 2026-11-07  
**Author:** Jonathan Korstad (`Jpalmer95` / `jkorstad`)  
**Status:** Implemented in `hacmdn` v0.2.0 Hermes Agent Plugin + Verified Pilot Models on Hugging Face

This document extends `03-spec-v0.1.md` with five architectural mechanisms from the original thesis that bridge the gap between a cold-start community network and a self-sustaining decentralized specialist swarm:

1. **The Neighborhood Connector Model (`qwen3-0.6b-neighborhood-connector-v1`)**
2. **Confidence-Weighted Bidding & Downstream Delegation Protocol (`§5.1b`)**
3. **The 6-Tier Progressive Upstream Escalation Ladder (`§5.5`)**
4. **Hugging Face Collection + ZeroGPU Community Load-Balancing Buffer (`§3.4`)**
5. **Community Governance Votes & Idle Open-Science / Local-Business Compute Pool (`§7.6`)**

---

## 1. Model #1: The Neighborhood Connector (`qwen3-0.6b-neighborhood-connector-v1`)

In `v0.1`, routing relied purely on organizer embedding indices (`kNN` over `task_descriptor`). While embedding retrieval works well for direct cosine matches, micro-specialists (`0.6B`) frequently encounter requests that sit at the boundary of their niche or require decomposing a request into a neighboring sub-niche.

The **Neighborhood Connector** is the first fine-tuned `Qwen/Qwen3-0.6B` specialist in every neighborhood. Its sole domain is **topological awareness and brutal-honesty triage**:
- Knows the heads of every niche family in its local neighborhood (`sql-analytics`, `code-synthesis`, `devops-infra`, `scientific-compute`, `local-business-ops`) and adjacent organizer bridges.
- Receives upstream handoffs whenever a micro-specialist abstains (`[ABSTAIN: OUT_OF_SCOPE]`).
- Outputs a deterministic JSON routing envelope:
  ```json
  {
    "status": "route" | "escalate" | "abstain",
    "inferred_domain": "sql",
    "target_neighborhood": "nbh-data-engineering",
    "recommended_specialist": "qwen3-0.6b-sql-window-rewriter-v1",
    "confidence": 0.91,
    "escalation_tier": 1,
    "bounty_proposal": null
  }
  ```

---

## 2. Confidence-Weighted Bidding & Downstream Proxy Bidding (`§5.1b`)

Instead of passive round-robin selection among top-$k$ candidates, HACMDN-Net introduces a **Confidence-Weighted Bidding Protocol**:

1. **Direct Specialist Bids:** Any worker node whose `spec_id` matches the domain tag or passes the organizer's `kNN` retrieval pre-filter submits a signed `Bid`:
   $$\text{BidScore}_i = \frac{\text{Conf}_i \cdot (\text{EvalScore}_i - \text{BaseScore}_i) \cdot (1 - \text{DivPenalty}_i)}{1 + \alpha \cdot (\text{Latency}_{p95,i} / 1000) + \beta \cdot \text{PriceCredits}_i}$$
   where:
   - $\text{Conf}_i \ge \tau_{\text{abstain}, i}$ (must clear the node's conformal abstention threshold, or the bid is disqualified).
   - $\text{EvalMargin}_i = \text{EvalScore}_i - \text{BaseScore}_i > 0$ (verified-on-entry gain over untouched `Qwen/Qwen3-0.6B`).
   - $\text{DivPenalty}_i \in [0, 0.5]$ penalizes near-duplicate adapters in recent ensemble/routing history (`arXiv:2502.00674`).

2. **Downstream Proxy Bids (Organizer / Connector Bidding on Behalf of a Micro-Model):**
   - A Neighborhood Connector or Organizer can submit a **Proxy Bid** on behalf of a downstream micro-specialist (`delegated_worker_id`) that is asleep, behind NAT, or registered under that neighborhood's custody.
   - If the proxy bid wins, the connector routes the payload to the downstream micro-model, verifies the response signature, and splits the escrowed task reward (`90%` worker / `10%` connector routing fee).

---

## 3. The 6-Tier Progressive Upstream Escalation Ladder (`§5.5`)

When a request enters HACMDN-Net via `hacmdn_route_query`, it walks a deterministic **Progressive Upstream Escalation Ladder** from smallest/cheapest local specialist up to larger models until a node clears its calibrated confidence bar:

| Tier | Node / Compute Layer | Model Size | Typical Latency | Trigger Condition |
|------|----------------------|------------|-----------------|-------------------|
| **Tier 0** | **Local Micro-Specialist** | `0.6B` LoRA | `40–180 ms` | Local node hosts a verified specialist whose domain matches & confidence $\ge \tau_{\text{abstain}}$. |
| **Tier 1** | **Neighborhood Connector + Peer Micro-Specialist** | `0.6B–1.7B` LoRA | `120–350 ms` | Tier 0 abstains or is absent; Neighborhood Connector maps task to a peer worker via the Bidding Protocol. |
| **Tier 2** | **Neighborhood Organizer Super-Peer** | `1.7B–4B` + `kNN` Index | `200–500 ms` | Local neighborhood lacks coverage; Organizer queries 2-hop cross-neighborhood gossip bridges. |
| **Tier 3** | **Hugging Face ZeroGPU Community Buffer** | `0.6B–4B` Hosted Space | `800–2500 ms` | An approved specialist exists in the HF Community Collection, but `0` P2P workers are currently online (`TTL` expired). |
| **Tier 4** | **Upstream Generalist / Frontier Node** | `14B+` (`Hermes-4-14B` / `ctx.llm`) | `1500–5000 ms` | No specialist in the network clears $\tau_{\text{abstain}}$, but the user requested immediate fallback completion. |
| **Tier 5** | **Structured Network Abstention + JIT Flywheel Bounty** | Protocol-level | `<10 ms` | Returned alongside Tier 4 (or standalone in strict specialist mode): logs the domain gap, increments demand counter, and opens a JIT fine-tuning bounty once demand crosses the threshold. |

---

## 4. Hugging Face Community Collection & ZeroGPU Buffer (`§3.4`)

A decentralized P2P network suffers from the **cold-start & diurnal churn problem**: early on, or at 3 AM, a niche specialist adapter may have zero live worker nodes online.

HACMDN-Net solves this with a two-part Hugging Face Hub integration:
1. **Canonical HF Community Collection (`jkorstad/hacmdn-net-hermes-specialist-network`):**
   - Stores all verified-on-entry LoRA adapters, their `capability_descriptor.json`, and canonical `eval_report.json`.
   - Every adapter follows the single-base-family rule (`Qwen/Qwen3-0.6B`, Apache-2.0) so `mergekit` DARE/TIES can combine same-domain adapters quarterly into a domain "neighborhood soup."
2. **ZeroGPU Community Buffer Space (`jkorstad/hacmdn-community-buffer`):**
   - A Gradio 6 + `@spaces.GPU` Space that dynamically loads approved LoRA adapters from the Community Collection on demand.
   - Acts as **Tier 3** in the escalation ladder: when every local/P2P worker for `qwen3-0.6b-sql-window-rewriter-v1` is offline, the plugin transparently routes to the ZeroGPU Buffer Space (or local GPU worker) so niche tasks never fail due to P2P churn.

---

## 5. Community Governance & Idle Compute Pool (`§7.6`)

When contributors opt in with spare GPU/CPU cycles and no paid client query is in flight:
1. **Community Directive Votes:** Node operators earn governance weight proportional to verified task completions (`reputation * sqrt(stake)`). Proposals rank which domain gaps (`bounties`) or public datasets should be prioritized next.
2. **Productive Idle Pool (Default Fallback):** When no paid request or active fine-tune bounty is queued, idle nodes pull micro-tasks from three community-curated pools:
   - `open-science`: protein/ligand descriptor formatting, literature citation verification, theorem lemma decomposition.
   - `local-business-aid`: menu/inventory normalization, local scheduling/schema extraction for small community businesses.
   - `network-calibration`: running holdout calibration probes and 5% sampling audit verifications to keep neighborhood conformal thresholds sharp.
