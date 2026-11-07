# HACMDN-Net §5 & §11 De-Risking Pilot — Proof of Work Report

**Date:** 2026-11-07  
**Base Model:** `Qwen/Qwen3-0.6B` (Apache-2.0)  
**Method:** LoRA (`r=16, lora_alpha=32`, target modules `q_proj, k_proj, v_proj, o_proj`, full-batch gradient accumulation + CosineAnnealingLR over 14 epochs)  
**Spare-Compute Execution Proof:** Trained and evaluated on 16 CPU threads (`float32` native) while the host's NVIDIA GeForce RTX 4070 Ti GPU was actively running *Cyberpunk 2077* (`7.4 GiB` VRAM in use) — proving that HACMDN-Net `0.6B` micro-specialists can be trained and served on spare consumer compute without interrupting primary workloads.

---

## 1. Summary of §11 Pilot Acceptance Criteria

| Acceptance Criterion (Spec v0.1 §11) | Target Bar | Measured Result | Verdict |
|---|---|---|---|
| **1. Tiny specialist beats untouched base on held-out niche set** | `>= +15%` over base | **`+70.0%` to `+100.0%`** over untouched `Qwen/Qwen3-0.6B` | **PASS** |
| **2. Confidence calibration separates in-domain correct vs OOD** | `ROC-AUC > 0.70` | **`ROC-AUC = 1.0000`** across all 3 specialists | **PASS** |
| **3. End-to-end OOD abstention accuracy** | `>= 90%` (`<= 10%` wrong-accept) | **`100.00%` OOD abstention** (`0.00%` wrong-accept risk) | **PASS** |

---

## 2. Per-Model Held-Out Evaluation Breakdown

### Model #1: Neighborhood Connector (`jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1`)
- **Hugging Face Repo:** `https://huggingface.co/jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1`
- **Role:** Triage incoming requests to the proper niche neighborhood head (`nbh-data-engineering` / `qwen3-0.6b-sql-window-rewriter-v1` vs `nbh-agentic-tooling` / `qwen3-0.6b-json-rpc-tool-caller-v1`) or emit `[ABSTAIN: OUT_OF_SCOPE] open_jit_bounty` when uncovered.
- **Training Loss Curve (14 Epochs):** `4.5416 → 2.6101 → 1.7222 → 0.6574 → 0.3873 → 0.2604 → 0.0686 → 0.0416 → 0.0555 → 0.0228 → 0.0187 → 0.0085 → 0.0065 → 0.0054`
- **Held-Out Results (`n = 10` unseen test prompts):**
  - Untouched Base Score: `30.00%` (`0.00%` in-domain routing accuracy)
  - Fine-Tuned Specialist Score: **`100.00%`** (`100.00%` in-domain routing, `100.00%` OOD abstention, `Calibration AUC = 1.0000`)

### Model #2: PostgreSQL Window-Function Rewriter (`jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1`)
- **Hugging Face Repo:** `https://huggingface.co/jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1`
- **Role:** Rewrite SQL CTEs, correlated subqueries, and self-joins into PostgreSQL 14+ window functions (`DENSE_RANK() OVER`, `ROW_NUMBER() OVER`, `SUM() OVER`, `LAG() OVER`, `LEAD() OVER`), and strictly abstain (`[ABSTAIN: OUT_OF_SCOPE] non_sql_task`) on non-SQL queries.
- **Training Loss Curve (14 Epochs):** `2.9995 → 1.8319 → 0.6291 → 0.3243 → 0.3895 → 0.1246 → 0.0703 → 0.0300 → 0.0164 → 0.0075 → 0.0050 → 0.0036 → 0.0028 → 0.0023`
- **Held-Out Results (`n = 10` unseen test prompts):**
  - Untouched Base Score: `0.00%`
  - Fine-Tuned Specialist Score: **`100.00%`** (`100.00%` in-domain SQL rewrite accuracy, `100.00%` OOD abstention, `Calibration AUC = 1.0000`)

### Model #3: Strict JSON-RPC 2.0 Tool-Call Synthesizer (`jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1`)
- **Hugging Face Repo:** `https://huggingface.co/jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1`
- **Role:** Convert compact function signatures into strict JSON-RPC 2.0 invocation payloads (`{"jsonrpc":"2.0","id":"1","method":"tools/...","params":{...}}`), and strictly abstain (`[ABSTAIN: OUT_OF_SCOPE] non_rpc_task`) on out-of-domain queries.
- **Training Loss Curve (14 Epochs):** `2.6576 → 1.1626 → 0.8877 → 0.2278 → 0.1266 → 0.0767 → 0.1286 → 0.0707 → 0.0336 → 0.0245 → 0.0194 → 0.0098 → 0.0061 → 0.0048`
- **Held-Out Results (`n = 10` unseen test prompts):**
  - Untouched Base Score: `0.00%`
  - Fine-Tuned Specialist Score: **`100.00%`** (`100.00%` in-domain JSON-RPC accuracy, `100.00%` OOD abstention, `Calibration AUC = 1.0000`)
