# AGENTS.md — HACMDN-Net (`hacmdn`)

Authoritative instructions for autonomous agents working on **HACMDN-Net** (*Hermes Agent Community Microtuned Decentralized Network Plugin*).

## Repository Overview

- **Repo Root:** `/home/jonathan/dev/hacmdn-net`
- **GitHub:** `https://github.com/Jpalmer95/hacmdn-net`
- **Installed Plugin Path:** `~/.hermes/plugins/hacmdn`
- **Durable State DB:** `~/.hermes/plugin-data/hacmdn/data.db` (via `plugins.plugin_storage.plugin_db("hacmdn")`)
- **Base Model Family:** `Qwen/Qwen3-0.6B` (Apache-2.0)
- **HF Models & Space:**
  - `jkorstad/hacmdn-qwen3-0.6b-neighborhood-connector-v1`
  - `jkorstad/hacmdn-qwen3-0.6b-sql-window-rewriter-v1`
  - `jkorstad/hacmdn-qwen3-0.6b-json-rpc-tool-caller-v1`
  - Space: `https://huggingface.co/spaces/jkorstad/hacmdn-community-buffer`

## Key Commands

```bash
# Validate the Hermes plugin (catalog CI + plugin doctor)
hermes plugins doctor /home/jonathan/dev/hacmdn-net --ci
hermes plugins validate /home/jonathan/dev/hacmdn-net

# Run the unit and integration test suite
pytest tests/ -q

# Run CLI commands once enabled
hermes hacmdn status
hermes hacmdn route "Rewrite this PostgreSQL CTE into a window function"
hermes hacmdn bounties
hermes hacmdn simulate

# Re-run the RTX 4070 Ti LoRA fine-tuning & §11 de-risking pilot evaluation
/mnt/flex/dev/calibre-tts-venv/bin/python3 training/run_pilot_experiment.py
```

## Plugin Architecture Rules

1. **Public Hermes Plugin Surfaces Only:** Use `ctx.register_tool`, `ctx.register_command`, `ctx.register_cli_command`, `ctx.register_skill`, `ctx.register_hook`, and `ctx.llm`. Never monkey-patch Hermes core modules.
2. **Handler Contract:** Every tool handler in `tools.py` must accept `(args: dict, **kwargs) -> str`, catch all exceptions, and return a JSON string.
3. **Durable State:** Never write runtime files inside the plugin install directory. Always use `plugin_data_dir("hacmdn")` / `plugin_db("hacmdn")`, with a clean fallback to `~/.hermes/plugin-data/hacmdn/` when running standalone tests outside Hermes.
4. **Eval Before Gossip:** Any specialist published via `hacmdn_publish_specialist` must beat `base_model_score + margin` on its canonical domain evaluation before entering the active gossip table.
5. **License:** Apache-2.0 (`Copyright 2026 Jonathan Korstad`).
