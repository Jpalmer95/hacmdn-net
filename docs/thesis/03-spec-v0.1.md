Hermes Specialist Network — Architecture Specification v0.1
Codename: HACMDN-Net ("Hermes Agent Community Microtuned Decentralized Network")
Status: Draft spec, informed by the feasibility report. Everything marked [greenfield] has no direct precedent; everything else cites one.

1. Design principles
Specialists over generalists. Every node runs something it is specifically good at, never a general model "just because."
Neighborhood, not router. No single point of task routing. Gossip + super-peers. (Petals DHT, exo topology gossip)
Knows when it doesn't know. Abstention is a first-class protocol response, not an error path.
Single base family. All tiny specialists derive from one base family (Qwen3, Apache-2.0) so mergekit can combine them later.
Eval before gossip. A capability claim is only trusted after the node passes the community's canonical eval for it. [greenfield]
Payments follow verified work. Escrowed per-task settlement; correctness via sampling audits, not trust.
2. Node model
Three node roles. Any machine can hold multiple roles.

2.1 Worker node
Runs 1–N tiny specialist models (0.6B–4B quantized; targets llama.cpp / MLX / vLLM serving).
Publishes a Capability Descriptor for each specialist (§4) into the gossip network.
Answers routed requests; signs responses; returns confidence metadata.
2.2 Organizer node (super-peer, a few per neighborhood)
Maintains the richest view of its neighborhood's capability graph (the "everyone knows mostly everyone, organizers know in depth" tier).
Runs the routing index: an embedding index over all received capability descriptors (Voyager-style skill retrieval; kNN-over-embeddings shown SOTA-simple for model routing, arXiv:2505.12601).
Hosts the calibration sets for the domains its neighborhood covers and re-scores node confidence periodically (§6).
Coordinates abstention escalation (§5.4) and proposes JIT fine-tune jobs to the community (§7).
Organizers are elected by stake + reputation, NOT appointed. Any worker can become an organizer by staking and passing the organizer readiness eval. Loss of all organizers degrades the neighborhood to pure-gossip mode (slower, still functional) — this is deliberate redundancy.
2.3 Client node
Any agent harness on the approved list (Hermes Agent first) with the plugin installed.
Submits requests through its nearest organizer or any peer it knows; receives either a routed answer, an abstention, or an escalation proposal.
3. Network topology & gossip
Layer 1 — DHT (control plane). A libp2p/Kademlia DHT. Every capability descriptor is published as (domain_tag, node_id) → Descriptor with a TTL of 10 minutes; workers refresh while serving. Churn is handled by expiry, exactly as Petals handles server liveness — no explicit offline signaling needed.

Layer 2 — Neighborhood gossip (data plane). Each worker maintains ~8 gossip peers + 1–2 organizers. Descriptor updates propagate via recursive gossip (depth-capped, exo-style collect_topology pattern). Organizers bridge neighborhoods, so a request that misses locally can still find a specialist two hops away.

Layer 3 — Request path. Client → nearest organizer index (kNN over descriptor embeddings + live load/latency filters) → chosen worker → signed response → settlement. Fallback path: client gossips the request to known peers directly when no organizer is reachable.

Load balancing & churn: organizers rebalance by routing away from nodes whose TTLs lapse or whose measured p95 latency degrades; Petals-style self-reselection lets idle workers choose to preload the specialists their neighborhood lacks (self-organizing capacity, precedent: Petals block_selection).

4. Capability Descriptor [greenfield — core IP]
The standardized, embeddable record every specialist publishes. This is what makes "who is good at what" computable.

{
  "spec_id": "qwen3-0.6b-sql-window-fns-v3",
  "base_model": "Qwen/Qwen3-0.6B",
  "adapter": "hf://datasets/.../or repo path",
  "task_descriptor": "Rewrites SQL using CTEs into equivalent window-function queries, PostgreSQL 14+ syntax only",
  "domains": ["sql", "postgres", "query-rewriting"],
  "input_schema": {"type": "sql_text", "max_len_tok": 512},
  "output_schema": {"type": "sql_text"},
  "eval_scores": {
    "canonical_eval": "sql-window-fns-v3-eval",
    "score": 0.87, "base_model_score": 0.31,
    "n_samples": 250, "eval_commit": "<sha>"
  },
  "calibration": {"abstain_threshold": 0.62, "calibrated_at": "2026-11-07", "coverage": 0.78},
  "diversity_fingerprint": "<embedding of task_descriptor + eval samples>",
  "serving": {"quant": "q4_k_m", "ctx_len": 4096, "p95_latency_ms": 340, "throughput_tok_s": 85},
  "identity": {"node_key": "<ed25519 pubkey>", "stake": 12.0},
  "ttl_expires": 1762516800,
  "license": "apache-2.0"
}
Design notes: task_descriptor is embedded for retrieval; diversity_fingerprint exists because heterogeneous ensembles can underperform homogeneous self-consistency (arXiv:2502.00674) — the index uses it to penalize routing to near-duplicate specialists; eval_scores are organizer-verified before gossip, closing the "capability fraud" gap.

5. Request lifecycle
5.1 Match
Client request → embed → kNN over organizer's descriptor index. Top-k candidates filtered by: live load, p95 latency, abstain-threshold headroom, and diversity penalty (avoid the three near-identical SQL specialists all taking turns).

5.2 Execute
Chosen worker runs inference. Response carries confidence (calibrated score) and spec_id provenance, signed.

5.3 Confidence & abstention
Worker returns semantic-entropy-based confidence: sample 3 short continuations, cluster by entailment, entropy over clusters (Confidence-Driven Router method, arXiv:2502.11021). Cost is bounded by sampling 3 continuations only on requests above a latency tier.
Network-level abstention: if the top candidate's confidence < its calibrated threshold, the organizer may try candidate #2; if none pass, it returns the abstention message (§5.4). Thresholds come from conformal calibration on the neighborhood's eval distribution (arXiv:2502.06884).
Unproven risk (flagged in feasibility report): semantic-entropy abstention quality at ≤1.7B sizes. The pilot measures it.
5.4 Abstention & escalation [greenfield]
Abstention is a structured response, not a failure:

{"status": "abstain",
 "reason": "no specialist covers <inferred domain>",
 "nearest": ["qwen3-0.6b-sql-window-fns-v3 (score 0.41)"],
 "proposal": {
   "gap": "sqlite query migration",
   "suggested_base": "Qwen/Qwen3-0.6B",
   "suggested_data": "user-provided pairs or synthetic",
   "est_cost_usd": 1.8, "est_hours": 2.5}}
Escalated gaps aggregate at organizers; when the same gap recurs across clients, the organizer opens a bounty: community members with GPUs claim it, fine-tune the missing specialist, submit it through verified-on-entry, and are paid from the bounty pool. This is the flywheel: abstentions are the demand signal, bounties are the supply response, descriptors are the compounding memory.

6. Calibration protocol [greenfield]
Each domain has a canonical eval set (community-curated, versioned, hash-pinned).
On entry, a worker runs the eval for every capability it claims. Scores below base_model_score + margin are rejected — the specialist must beat the untouched base or its descriptor is never gossiped.
Organizers periodically send probing requests (holdout items) and record (confidence, correctness) pairs; per-specialist abstain thresholds are fit to hit the neighborhood's target risk level (calibration-on-deployment-distribution requirement, arXiv:2502.04428).
Probes double as the sampling audit stream (§8), so the cost of calibration and of verification is one mechanism, not two.
7. JIT fine-tuning flywheel
Abstention log → organizer clusters recurring gaps.
Gap passes a threshold (frequency × demand × absence of coverage) → bounty opened.
A contributor (or ML Intern / similar agent harness) claims it: builds/collects data, fine-tunes on the standard base family, submits adapter + descriptor.
Verified-on-entry runs; if it beats base by the margin, descriptor enters gossip, bounty pays, and the abstention class routes there from then on.
Quarterly, mergekit combines same-domain specialists (DARE/TIES) into a "neighborhood soup" — a free generalist for the domain, requiring the single-base-family constraint of Principle 4.
Approved-model policy: an allowlist of base models (start: Qwen3-0.6B/1.7B/4B; Hermes-4-14B for bigger nodes) and signed adapters. New base families enter by community vote + eval.

8. Payments & verification
Admission: stake-gated (sybil resistance, Akash/Hyperbolic pattern). Stake is slashable.
Settlement: escrowed per-task; released on acceptance; streaming for long jobs.
Correctness (the unsolved industry problem — none of io.net/Akash/Render/Golem verify outputs):
Sampling audits: organizer re-routes a random ~5% of requests to a second worker; agreement within tolerance → pay both; disagreement → challenge.
Challenge period: requester or bounty hunters can dispute within 24h; disputed work is re-computed by a stake-gated third node (Petals pledged-audit design, arXiv:2209.01188).
Losses paid from the disputing loser's stake. zkML is deliberately out of scope v0.1 (not yet practical at these sizes).
Contributor rewards: per-task payment for workers; bounty payment for fine-tuners; calibration probe payment small but non-zero (keeps probe supply honest).
9. Security model
Threat	Vector	Control
Capability fraud	node claims skills it lacks	Eval-before-gossip (§6.2); organizer probes
Garbage output	lazy or malicious worker	Sampling audits + challenge period + slashing (§8)
Sybil	farm payments with fake nodes	Stake gate; payments only post-verified completions
Data exfiltration	node operator sees prompts	Reputation tiers; privacy tier routes to attested nodes only; TEEs post-v0.1
Supply chain	malicious plugin/harness	Approved-harness allowlist; signed plugin releases; descriptor schema versioning
Router capture	organizers collude on routing	Election by stake+reputation; clients can always fall back to direct gossip path; organizer decisions reproducible from the public descriptor log
Eval poisoning	canonical evals gamed	Evals versioned + hash-pinned; holdout splits rotated by organizers
10. Plugin interface (what the prototype implements)
class HermesSpecialistPlugin:
    def start(config) -> None                 # join gossip, publish descriptors, start serving
    def publish(descriptor: CapabilityDescriptor)  # register a local specialist
    def query(request: str) -> Response | Abstain   # full §5 lifecycle
    def on_abstain(callback)                  # harness hook: show escalation proposal
    def claim_bounty(bounty_id) -> JobSpec    # JIT flywheel participation
    def status() -> NetworkStatus             # neighbors, organizers, local models
Storage: local descriptor cache (SQLite), model registry directory, key store. No cloud dependency for the MVP control path.

11. Pilot acceptance criteria
The pilot fine-tune (next step) validates the riskiest claims before any network code hardens:

Tiny specialist (Qwen3-0.6B or 1.7B, LoRA, single GPU) beats both its untouched base and a strong generalist on a niche task's held-out set.
Semantic-entropy confidence actually separates correct from incorrect answers at 0.6B (calibration AUC > 0.7 is the bar).
End-to-end abstention: out-of-domain requests correctly abstain ≥90% of the time at ≤10% wrong-accept risk.
If 1 fails → thesis revisit. If 2 fails → fall back to redundant-agreement confidence. If 3 fails → conformal threshold retuning on more probes.
