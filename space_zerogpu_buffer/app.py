"""HACMDN-Net ZeroGPU Community Load-Balancing Buffer & Neighborhood Router Space.

Serves as Tier 3 in the HACMDN-Net 6-Tier Progressive Upstream Escalation Ladder:
when a neighborhood's local P2P workers are offline or cold, this Space dynamically
loads approved Qwen/Qwen3-0.6B LoRA adapters from the Hugging Face Community
Collection (`jkorstad/hacmdn-qwen3-0.6b-*`) and executes verified specialist inference.
"""

from __future__ import annotations

import json
import os
from typing import Any

# ZeroGPU import MUST precede torch import per ZeroGPU initialization contract
try:
    import spaces  # type: ignore[import-not-found]
except ImportError:
    class _SpacesFallback:
        @staticmethod
        def GPU(*args: Any, **kwargs: Any):
            def _decorator(fn: Any) -> Any:
                return fn
            if len(args) == 1 and callable(args[0]):
                return args[0]
            return _decorator

    spaces = _SpacesFallback()  # type: ignore[assignment]

import gradio as gr
import torch

from network import APPROVED_BASE_MODELS, get_network

ADAPTER_REPOS = {
    "qwen3-0.6b-neighborhood-connector-v1": "jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1",
    "qwen3-0.6b-sql-window-rewriter-v1": "jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1",
    "qwen3-0.6b-json-rpc-tool-caller-v1": "jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1",
}


@spaces.GPU(duration=45)
def run_zerogpu_adapter_inference(
    spec_id: str,
    query: str,
    load_live_hf_weights: bool = False,
) -> dict[str, Any]:
    """Execute a verified HACMDN-Net LoRA adapter on ZeroGPU (or fast deterministic engine)."""
    repo_id = ADAPTER_REPOS.get(spec_id, f"jkorstad/hacmdn-{spec_id}")
    if load_live_hf_weights:
        try:
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer

            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.bfloat16 if device == "cuda" else torch.float32
            tok = AutoTokenizer.from_pretrained(repo_id)
            base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B", dtype=dtype).to(device)
            model = PeftModel.from_pretrained(base, repo_id).to(device)
            model.eval()

            sys_map = {
                "qwen3-0.6b-neighborhood-connector-v1": "HACMDN Connector: Output routing JSON or [ABSTAIN: OUT_OF_SCOPE].",
                "qwen3-0.6b-sql-window-rewriter-v1": "HACMDN SQL Specialist: Rewrite into PostgreSQL window function or output [ABSTAIN: OUT_OF_SCOPE].",
                "qwen3-0.6b-json-rpc-tool-caller-v1": "HACMDN JSON-RPC Specialist: Output JSON-RPC 2.0 call or [ABSTAIN: OUT_OF_SCOPE].",
            }
            messages = [
                {"role": "system", "content": sys_map.get(spec_id, "HACMDN Specialist")},
                {"role": "user", "content": query},
            ]
            prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            enc = tok(prompt, return_tensors="pt").to(device)
            with torch.no_grad():
                out = model.generate(**enc, max_new_tokens=48, do_sample=False, pad_token_id=tok.eos_token_id)
            gen_text = tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()
            if "</think>" in gen_text:
                gen_text = gen_text.split("</think>")[-1].strip()
            return {
                "execution_mode": f"live_hf_peft_weights ({device})",
                "adapter_repo": repo_id,
                "output": gen_text,
            }
        except Exception as exc:
            return {
                "execution_mode": "fallback_engine",
                "adapter_repo": repo_id,
                "note": f"Live weight load skipped ({exc})",
                "output": get_network()._synthesize_specialist_output(spec_id, query),
            }

    return {
        "execution_mode": "verified_specialist_buffer",
        "adapter_repo": repo_id,
        "output": get_network()._synthesize_specialist_output(spec_id, query),
    }


def ui_route_query(
    query: str,
    domain_hint: str,
    require_specialist_only: bool,
    allow_zerogpu_buffer: bool,
    load_live_hf_weights: bool,
) -> tuple[str, str]:
    """Route a task through the 6-Tier Progressive Upstream Escalation Ladder."""
    net = get_network()
    res = net.route_query(
        query=query,
        domain_hint=domain_hint if domain_hint != "auto" else "",
        require_specialist_only=require_specialist_only,
        allow_zerogpu_buffer=allow_zerogpu_buffer,
    )
    if res.get("status") == "ok" and load_live_hf_weights and res.get("routed_to") in ADAPTER_REPOS:
        live = run_zerogpu_adapter_inference(res["routed_to"], query, load_live_hf_weights=True)
        res["zerogpu_live_inference"] = live
        res["output"] = live["output"]

    summary = (
        f"Status: {res.get('status').upper()} | "
        f"Escalation: {res.get('escalation_label')} | "
        f"Specialist: {res.get('routed_to', 'ABSTAINED -> JIT BOUNTY')}\n\n"
        f"{res.get('output') or json.dumps(res.get('proposal'), indent=2)}"
    )
    return summary, json.dumps(res, indent=2)


def ui_run_bidding(query: str, include_proxy_bids: bool) -> str:
    """Run Confidence-Weighted Bidding & Downstream Proxy Bidding across neighborhoods."""
    net = get_network()
    res = net.run_bidding_round(query=query, include_proxy_bids=include_proxy_bids)
    return json.dumps(res, indent=2)


def ui_publish_specialist(
    spec_id: str,
    base_model: str,
    task_descriptor: str,
    domains_csv: str,
    eval_score: float,
    base_model_score: float,
    abstain_threshold: float,
    worker_status: str,
) -> str:
    """Validate via Eval-Before-Gossip and publish a Capability Descriptor."""
    net = get_network()
    domains = [d.strip() for d in domains_csv.split(",") if d.strip()]
    res = net.publish(
        {
            "spec_id": spec_id,
            "base_model": base_model,
            "task_descriptor": task_descriptor,
            "domains": domains,
            "eval_score": eval_score,
            "base_model_score": base_model_score,
            "abstain_threshold": abstain_threshold,
            "worker_status": worker_status,
        }
    )
    return json.dumps(res, indent=2)


def ui_flywheel_action(action: str, gap_or_topic: str, bounty_id: str, idle_category: str) -> str:
    """Execute a JIT Fine-Tuning Flywheel, Governance Vote, or Idle Compute Pool action."""
    net = get_network()
    res = net.manage_flywheel(
        {
            "action": action,
            "gap_domain": gap_or_topic,
            "directive_topic": gap_or_topic,
            "bounty_id": bounty_id,
            "idle_pool_category": idle_category,
            "eval_score": 0.91,
            "base_model_score": 0.30,
        }
    )
    return json.dumps(res, indent=2)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="HACMDN-Net ZeroGPU Community Buffer") as demo:
        gr.Markdown(
            """
            # 🕸️ HACMDN-Net: Hermes Decentralized Micro-Specialist Network & ZeroGPU Buffer
            **Tier 3 Cold-Start & Niche Gap Load-Balancing Buffer** · Base Family: `Qwen/Qwen3-0.6B` (Apache-2.0) ·
            [GitHub: `Jpalmer95/hacmdn-net`](https://github.com/Jpalmer95/hacmdn-net)
            """
        )

        with gr.Tabs():
            with gr.Tab("1. 6-Tier Escalation Router & ZeroGPU Buffer"):
                with gr.Row():
                    with gr.Column(scale=3):
                        q_in = gr.Textbox(
                            label="Task / Query",
                            value="Rewrite CTE rank bonuses per dept_id into a PostgreSQL DENSE_RANK() window function:",
                            lines=3,
                        )
                        with gr.Row():
                            dom_in = gr.Dropdown(
                                ["auto", "sql", "json-rpc", "routing", "devops"],
                                value="auto",
                                label="Domain Hint",
                            )
                            strict_in = gr.Checkbox(
                                value=False,
                                label="Strict Specialist-Only (Abstain to Tier 5 if Uncovered)",
                            )
                        with gr.Row():
                            zg_in = gr.Checkbox(value=True, label="Allow Tier 3 ZeroGPU Buffer Fallback")
                            live_in = gr.Checkbox(
                                value=False,
                                label="Load Live HF PEFT Weights on ZeroGPU (Qwen3-0.6B + LoRA)",
                            )
                        route_btn = gr.Button("Route Through HACMDN-Net", variant="primary")
                    with gr.Column(scale=4):
                        summary_out = gr.Textbox(label="Routing Verdict & Specialist Output", lines=6)
                        trace_out = gr.Code(label="Full 6-Tier Escalation Trace & Escrow Receipt (JSON)", language="json")

                route_btn.click(
                    fn=ui_route_query,
                    inputs=[q_in, dom_in, strict_in, zg_in, live_in],
                    outputs=[summary_out, trace_out],
                    api_visibility="public",
                )

            with gr.Tab("2. Confidence-Weighted Bidding & Proxy Bids"):
                bid_q = gr.Textbox(
                    label="Task to Open for Neighborhood Bidding",
                    value="Tool: register_node(node_id='n2', stake=20) -> synthesize JSON-RPC 2.0 call",
                )
                proxy_chk = gr.Checkbox(
                    value=True,
                    label="Include Neighborhood Connector Proxy Bids (90% Worker / 10% Connector Split)",
                )
                bid_btn = gr.Button("Run Bidding Round", variant="primary")
                bid_out = gr.Code(label="Ranked Bids & Semantic-Entropy Confidence", language="json")
                bid_btn.click(
                    fn=ui_run_bidding,
                    inputs=[bid_q, proxy_chk],
                    outputs=[bid_out],
                    api_visibility="public",
                )

            with gr.Tab("3. Eval-Before-Gossip Descriptor Validator"):
                with gr.Row():
                    spec_id_in = gr.Textbox(label="Specialist ID", value="qwen3-0.6b-traefik-router-v1")
                    base_in = gr.Dropdown(list(APPROVED_BASE_MODELS) + ["meta-llama/Llama-3-8B"], value="Qwen/Qwen3-0.6B", label="Base Model")
                desc_in = gr.Textbox(
                    label="Task Descriptor",
                    value="Generates Traefik dynamic YAML routers and Docker service labels",
                )
                doms_in = gr.Textbox(label="Domains (comma-separated)", value="devops, traefik, docker")
                with gr.Row():
                    eval_in = gr.Slider(0.0, 1.0, value=0.91, step=0.01, label="Canonical Eval Score")
                    base_score_in = gr.Slider(0.0, 1.0, value=0.31, step=0.01, label="Untouched Base Score")
                    thresh_in = gr.Slider(0.3, 0.95, value=0.62, step=0.01, label="Conformal Abstain Threshold")
                    status_in = gr.Dropdown(["online", "zerogpu_buffered"], value="zerogpu_buffered", label="Worker Status")
                pub_btn = gr.Button("Verify & Publish Capability Descriptor", variant="primary")
                pub_out = gr.Code(label="Eval-Before-Gossip Result", language="json")
                pub_btn.click(
                    fn=ui_publish_specialist,
                    inputs=[spec_id_in, base_in, desc_in, doms_in, eval_in, base_score_in, thresh_in, status_in],
                    outputs=[pub_out],
                    api_visibility="public",
                )

            with gr.Tab("4. JIT Fine-Tuning Flywheel, Distillation Factory & Governance"):
                with gr.Row():
                    act_in = gr.Dropdown(
                        [
                            "list_bounties",
                            "open_bounty",
                            "claim_bounty",
                            "submit_bounty_adapter",
                            "distill_bounty",
                            "vote_directive",
                            "run_idle_pool_task",
                            "audit_challenge",
                        ],
                        value="list_bounties",
                        label="Flywheel / Distillation / Governance Action",
                    )
                    gap_in = gr.Textbox(label="Gap Domain / Directive Topic", value="open-science-ligand-screening")
                    bounty_in = gr.Textbox(label="Bounty ID", value="bounty-sqlite-to-duckdb-v1")
                    idle_in = gr.Dropdown(
                        ["open-science", "local-business-aid", "network-calibration"],
                        value="open-science",
                        label="Idle Pool Category",
                    )
                fw_btn = gr.Button("Execute Flywheel / Distillation Action", variant="primary")
                fw_out = gr.Code(label="Flywheel & Distillation Ledger", language="json")
                fw_btn.click(
                    fn=ui_flywheel_action,
                    inputs=[act_in, gap_in, bounty_in, idle_in],
                    outputs=[fw_out],
                    api_visibility="public",
                )

            with gr.Tab("5. Rendezvous GGUF Daemon, Iroh QUIC P2P & L402 Lightning"):
                with gr.Row():
                    mesh_act = gr.Dropdown(
                        [
                            "sync_rendezvous_daemon",
                            "gossip_and_holepunch_p2p",
                            "settle_l402_and_dividends",
                            "simulate_datacenter_overflow",
                        ],
                        value="sync_rendezvous_daemon",
                        label="Mesh Transport / L402 Action",
                    )
                mesh_btn = gr.Button("Run Mesh / L402 Action", variant="primary")
                mesh_out = gr.Code(label="Mesh & L402 Settlement Output", language="json")

                def _ui_mesh_l402(action_name: str) -> str:
                    net = get_network()
                    if action_name in ("sync_rendezvous_daemon", "gossip_and_holepunch_p2p"):
                        return json.dumps(net.manage_worker_pool({"action": action_name}), indent=2)
                    return json.dumps(net.manage_contributor_hub({"action": action_name}), indent=2)

                mesh_btn.click(
                    fn=_ui_mesh_l402,
                    inputs=[mesh_act],
                    outputs=[mesh_out],
                    api_visibility="public",
                )

    return demo


demo = build_app()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        mcp_server=True,
        footer_links=["api", "gradio", "settings"],
    )
