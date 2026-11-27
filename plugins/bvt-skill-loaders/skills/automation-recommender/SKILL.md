---
name: "automation-recommender"
description: "Analyze a codebase and recommend automations: hooks, subagents, skills, plugins and MCP servers. Use when asked for automation recommendations or how to set up an AI coding setup for a project. Read-only; from the official claude-code-setup plugin."
---

# Automation Recommender (claude-code-setup)

The full skill (instructions and references for hooks, skills, subagents, plugins and MCP servers) lives in Anthropic's official plugin repo, anthropics/claude-plugins-official, pinned to commit `0412be76f50ab4f4f8abff3753efa9269fbbca5b`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/automation-recommender"; P=plugins/claude-code-setup/skills/claude-automation-recommender
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/anthropics/claude-plugins-official 0412be76f50ab4f4f8abff3753efa9269fbbca5b && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`references/...`) resolve against the skill folder.
- It is read-only: analyze and recommend, never create or change files unless the user asks separately.
- When the user works in this chat rather than the Claude Code terminal, say which recommendations apply here (skills, connectors/MCP servers) and which need Claude Code (hooks, subagents, settings files).
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.