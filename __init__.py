"""HACMDN-Net (`hacmdn`) — Hermes Agent Community Microtuned Decentralized Network Plugin."""

from __future__ import annotations

from pathlib import Path

try:
    from . import cli_commands, schemas, tools
except ImportError:
    import cli_commands  # type: ignore[no-redef]
    import schemas  # type: ignore[no-redef]
    import tools  # type: ignore[no-redef]

TOOLSET = "hacmdn"

_TOOLS = (
    ("hacmdn_route_query",        schemas.HACMDN_ROUTE_QUERY,        tools.hacmdn_route_query,        "🕸️"),
    ("hacmdn_publish_specialist", schemas.HACMDN_PUBLISH_SPECIALIST, tools.hacmdn_publish_specialist, "📡"),
    ("hacmdn_bid_task",           schemas.HACMDN_BID_TASK,           tools.hacmdn_bid_task,           "⚖️"),
    ("hacmdn_bounty_flywheel",    schemas.HACMDN_BOUNTY_FLYWHEEL,    tools.hacmdn_bounty_flywheel,    "🎯"),
    ("hacmdn_network_status",     schemas.HACMDN_NETWORK_STATUS,     tools.hacmdn_network_status,     "🗺️"),
)


def register(ctx) -> None:
    """Register HACMDN-Net tools, slash command, CLI subcommand, and bundled skill."""
    for name, schema, handler, emoji in _TOOLS:
        ctx.register_tool(
            name=name,
            toolset=TOOLSET,
            schema=schema,
            handler=handler,
            emoji=emoji,
        )

    ctx.register_command(
        "hacmdn",
        handler=cli_commands.handle_slash_command,
        description="Inspect or route tasks across the HACMDN-Net decentralized micro-specialist network",
        args_hint="[status|route|bid|bounties|vote|idle]",
    )

    ctx.register_cli_command(
        name="hacmdn",
        help="Manage and query the HACMDN-Net decentralized micro-specialist network",
        setup_fn=cli_commands.setup_cli_parser,
        handler_fn=cli_commands.handle_cli_command,
    )

    skills_dir = Path(__file__).parent / "skills"
    if skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.is_file():
                ctx.register_skill(child.name, skill_md)


__all__ = ["register"]
