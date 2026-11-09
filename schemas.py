"""Tool schemas for the HACMDN-Net Hermes Agent Plugin."""

from __future__ import annotations

HACMDN_ROUTE_QUERY = {
    "name": "hacmdn_route_query",
    "description": (
        "Route a specialized task or query through the HACMDN-Net decentralized specialist neighborhood. "
        "Runs the Neighborhood Connector, executes a confidence-weighted bidding round across tiny fine-tuned "
        "Qwen3 specialists (0.6B-4B), evaluates semantic-entropy confidence against conformal abstention "
        "thresholds, and progressively escalates upstream (Tier 0 Local Micro-Specialist -> Tier 1 Neighborhood "
        "Connector + Peer Bid -> Tier 2 Organizer Super-Peer -> Tier 3 Hugging Face ZeroGPU Buffer -> Tier 4 "
        "Upstream Generalist -> Tier 5 Structured Abstention + JIT Fine-Tuning Bounty Proposal)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The prompt, SQL query, function spec, or task to route to a specialist.",
            },
            "domain_hint": {
                "type": "string",
                "description": (
                    "Optional domain tag hint (e.g. 'sql', 'postgres', 'json-rpc', 'tool-calling', 'routing'). "
                    "When omitted, the Neighborhood Connector infers the domain automatically."
                ),
            },
            "require_specialist_only": {
                "type": "boolean",
                "description": (
                    "If true, strictly abstain (Tier 5) when no verified micro-specialist clears its calibrated "
                    "confidence threshold rather than escalating to a generalist. Default: false."
                ),
            },
            "allow_zerogpu_buffer": {
                "type": "boolean",
                "description": (
                    "If true (default), allow routing to the Hugging Face ZeroGPU Community Buffer Space when "
                    "matching P2P worker nodes have expired TTLs or are offline."
                ),
            },
            "execute_live_model": {
                "type": "boolean",
                "description": (
                    "If true, execute real model weights (local LoRA checkpoint or live ZeroGPU Space endpoint) "
                    "when available. Default: true."
                ),
            },
        },
        "required": ["query"],
    },
}

HACMDN_PUBLISH_SPECIALIST = {
    "name": "hacmdn_publish_specialist",
    "description": (
        "Validate and publish a tiny fine-tuned specialist's Capability Descriptor into the HACMDN-Net "
        "neighborhood gossip table. Enforces Principle 4 (approved base model family, e.g. Qwen/Qwen3-0.6B) "
        "and Principle 5 (Eval-Before-Gossip: canonical eval score must beat untouched base_model_score by "
        "at least +0.15 margin). Computes the diversity fingerprint and registers the node."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "spec_id": {
                "type": "string",
                "description": "Unique specialist identifier (e.g., 'qwen3-0.6b-sql-window-rewriter-v1').",
            },
            "base_model": {
                "type": "string",
                "description": "Base model ID from the approved family (default: 'Qwen/Qwen3-0.6B').",
            },
            "adapter": {
                "type": "string",
                "description": "Hugging Face repo ID or URI for the LoRA adapter (e.g. 'hf://jkorstad/...').",
            },
            "task_descriptor": {
                "type": "string",
                "description": "Clear, embeddable description of the narrow task this specialist excels at.",
            },
            "domains": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of domain tags (e.g., ['sql', 'postgres', 'query-rewriting']).",
            },
            "canonical_eval": {
                "type": "string",
                "description": "Name of the community canonical benchmark used for verification.",
            },
            "eval_score": {
                "type": "number",
                "description": "Specialist accuracy/score on the canonical eval (0.0 to 1.0).",
            },
            "base_model_score": {
                "type": "number",
                "description": "Untouched base model score on the same canonical eval (0.0 to 1.0).",
            },
            "abstain_threshold": {
                "type": "number",
                "description": "Calibrated conformal abstention threshold (0.0 to 1.0, default 0.62).",
            },
            "neighborhood_id": {
                "type": "string",
                "description": "Target neighborhood cluster ID (e.g. 'nbh-data-engineering').",
            },
            "p95_latency_ms": {
                "type": "integer",
                "description": "Measured p95 inference latency in milliseconds (default 180).",
            },
            "stake": {
                "type": "number",
                "description": "Staked network credits backing this worker's honesty (default 15.0).",
            },
            "worker_status": {
                "type": "string",
                "enum": ["online", "zerogpu_buffered", "offline"],
                "description": "Serving state of the worker node (default 'online').",
            },
        },
        "required": [
            "spec_id",
            "task_descriptor",
            "domains",
            "eval_score",
            "base_model_score",
        ],
    },
}

HACMDN_BID_TASK = {
    "name": "hacmdn_bid_task",
    "description": (
        "Run a transparent HACMDN-Net Confidence-Weighted Bidding round for a task across all local, "
        "peer, and proxy-bidding Neighborhood Connector nodes without executing the final generation. "
        "Returns ranked bids, calibrated semantic-entropy confidence estimates, diversity penalties, "
        "and whether any Neighborhood Connector bid on behalf of a downstream micro-model."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Task description or prompt to open for neighborhood bidding.",
            },
            "domain_hint": {
                "type": "string",
                "description": "Optional domain tag filter.",
            },
            "include_proxy_bids": {
                "type": "boolean",
                "description": "Include upstream Neighborhood Connector proxy bids on behalf of downstream models (default: true).",
            },
        },
        "required": ["query"],
    },
}

HACMDN_BOUNTY_FLYWHEEL = {
    "name": "hacmdn_bounty_flywheel",
    "description": (
        "Interact with the HACMDN-Net JIT Fine-Tuning Flywheel, Community Governance Votes, and Idle "
        "Open-Science / Local-Business Compute Pool. Actions: 'list_bounties', 'open_bounty', 'claim_bounty', "
        "'submit_bounty_adapter', 'vote_directive', 'run_idle_pool_task', 'audit_challenge'."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "list_bounties",
                    "open_bounty",
                    "claim_bounty",
                    "submit_bounty_adapter",
                    "vote_directive",
                    "run_idle_pool_task",
                    "audit_challenge",
                ],
                "description": "Flywheel or governance operation to execute.",
            },
            "bounty_id": {
                "type": "string",
                "description": "Bounty ID for 'claim_bounty' or 'submit_bounty_adapter'.",
            },
            "gap_domain": {
                "type": "string",
                "description": "Domain gap description when opening a new fine-tuning bounty.",
            },
            "reward_credits": {
                "type": "number",
                "description": "Bounty reward in network credits (default 25.0).",
            },
            "contributor_id": {
                "type": "string",
                "description": "Node or contributor handle claiming a bounty or voting (default 'jkorstad-node-01').",
            },
            "adapter_repo": {
                "type": "string",
                "description": "HF adapter repo submitted to fulfill a bounty.",
            },
            "eval_score": {
                "type": "number",
                "description": "Eval score achieved by the submitted bounty adapter.",
            },
            "base_model_score": {
                "type": "number",
                "description": "Base model score on the bounty benchmark.",
            },
            "directive_topic": {
                "type": "string",
                "description": "Community directive or open-science priority to vote for.",
            },
            "idle_pool_category": {
                "type": "string",
                "enum": ["open-science", "local-business-aid", "network-calibration"],
                "description": "Category for 'run_idle_pool_task' when spare compute is donated.",
            },
            "task_receipt_id": {
                "type": "string",
                "description": "Receipt ID to audit or challenge under 'audit_challenge'.",
            },
        },
        "required": ["action"],
    },
}

HACMDN_NETWORK_STATUS = {
    "name": "hacmdn_network_status",
    "description": (
        "Inspect the live state of the HACMDN-Net decentralized specialist network: active neighborhoods, "
        "organizer super-peers, registered Qwen3 micro-specialists, capability descriptors, ZeroGPU buffer "
        "status, Hugging Face Community Collection links, escrow/stake ledger, and recent abstention gaps."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "neighborhood_id": {
                "type": "string",
                "description": "Optional filter by neighborhood ID.",
            },
            "include_descriptors": {
                "type": "boolean",
                "description": "If true, include full Capability Descriptor JSON records (default: true).",
            },
        },
        "required": [],
    },
}

HACMDN_WORKER_POOL = {
    "name": "hacmdn_worker_pool",
    "description": (
        "Manage this machine's participation in the HACMDN-Net decentralized compute mesh. "
        "Profiles local CPU/RAM/GPU hardware with Game-Guard (never interrupting active games/renders), "
        "computes Neighborhood Shortage Scores to auto-select which niche Qwen3-0.6B specialist is needed most, "
        "allocates compute across the 4 work pools ('pool-interactive-micro', 'pool-parallel-batch', "
        "'pool-idle-community', 'pool-jit-finetune'), or runs a parallel multi-query batch across the mesh."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "profile_and_recommend",
                    "configure_worker",
                    "auto_load_needed_specialist",
                    "run_parallel_batch",
                ],
                "description": "Worker pool operation to run.",
            },
            "compute_mode": {
                "type": "string",
                "enum": ["auto_game_guard", "spare_cpu_only", "gpu_when_idle", "paused"],
                "description": "Compute contribution mode for 'configure_worker'.",
            },
            "subscribed_pools": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Work pools this node opts into (e.g. ['pool-interactive-micro', 'pool-idle-community']).",
            },
            "batch_queries": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of sub-tasks/queries to execute concurrently in 'run_parallel_batch'.",
            },
        },
        "required": ["action"],
    },
}

HACMDN_CONTRIBUTOR_HUB = {
    "name": "hacmdn_contributor_hub",
    "description": (
        "Access the HACMDN-Net Contributor & Node Operator Hub: view accumulated earnings and the "
        "70/10/10/10 Shared-Entity Attribution breakdown (Worker Inference + Adapter Author Royalties + "
        "Connector Routing + Shared Community Pool), check the Anti-Whale Daily Cap & Datacenter Overflow "
        "Dividend Pool, pitch a new idea/directive to the community, or render the interactive GUI Hub."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "get_hub_snapshot",
                    "pitch_idea",
                    "simulate_datacenter_overflow",
                    "export_gui_widget",
                ],
                "description": "Hub action to perform.",
            },
            "operator_id": {
                "type": "string",
                "description": "Contributor/operator ID (default 'jkorstad-node-01').",
            },
            "idea_title": {
                "type": "string",
                "description": "Short title when pitching a new community directive or niche specialist idea.",
            },
            "idea_description": {
                "type": "string",
                "description": "Detailed description of the community idea, open-science goal, or local-business aid proposal.",
            },
            "idea_category": {
                "type": "string",
                "enum": ["niche-specialist", "open-science", "local-business-aid", "protocol-governance"],
                "description": "Category for 'pitch_idea'.",
            },
            "raw_datacenter_credits": {
                "type": "number",
                "description": "Raw compute credits contributed by a large cluster in 'simulate_datacenter_overflow' (e.g. 120.0) to demonstrate the Anti-Whale Community Cap.",
            },
        },
        "required": ["action"],
    },
}
