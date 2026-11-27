---
name: "reverse-engineer-anything"
description: "Reverse engineer shipped apps and binaries with REA: native, Electron/JavaScript, Android, packaged, firmware and browser targets. Use to explain features, compare versions or decompile. Skip for normal source-code repos."
---

# REA (Reverse Engineer Anything)

The full skill (instructions and per-target references) lives on GitHub at morluto/rea, pinned to commit `144843ccc26bd372d61b8c6a27b37a01a5b0fb61`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/reverse-engineer-anything"; P=.agents/skills/reverse-engineer-anything
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/morluto/rea 144843ccc26bd372d61b8c6a27b37a01a5b0fb61 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`references/...`) resolve against the skill folder.
- When no REA MCP tools (`mcp__rea__*`) are connected, use the command-line form it describes: `npx -y rea-agents@latest <command>`.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.