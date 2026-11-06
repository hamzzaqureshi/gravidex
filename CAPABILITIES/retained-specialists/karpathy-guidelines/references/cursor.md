# Using Karpathy Guidelines with Cursor

This capability includes the Karpathy-inspired behavioral guidelines that can apply automatically when you work in Cursor.

## In this repository

1. The behavioral guidelines apply automatically through Antigravity, Claude Code, and OpenCode.
2. In Cursor, you can configure project rules under **Settings -> Rules**, where `karpathy-guidelines` can be added.

## Use the same guidelines in another project

**Cursor:** Copy the rule into that project's `.cursor/rules/` directory (create the folders if needed). Adjust or merge with existing rules as you like.

**Other tools:** If a stack only supports a root instruction file, copy [`claude.md`](claude.md) into that project instead (or merge its contents into your existing instructions).

## Optional: personal Agent Skills

If you want the same content as a reusable skill under `~/.cursor/skills`, use [`../SKILL.md`](../SKILL.md). You can copy or symlink it into your personal skills directory; use whatever layout you use for other skills.

## Claude Code vs Cursor

- **Claude Code:** Install via the GraviDex capability suite. Per-project use can also rely on [`claude.md`](claude.md).
- **Cursor:** Use the committed `.cursor/rules/` file. Cursor does not read `.claude-plugin/` or `CLAUDE.md` by default.

## For contributors

When you change the four principles, keep [`claude.md`](claude.md) and [`../SKILL.md`](../SKILL.md) in sync.
