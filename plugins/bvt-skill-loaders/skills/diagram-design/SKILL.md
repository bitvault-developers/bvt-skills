---
name: "diagram-design"
description: "Create editorial technical diagrams as HTML/SVG/PNG: architecture, flowchart, sequence, state, ER/schema, timeline, swimlane, org chart, Sankey, Gantt, journey, deployment and more, with Mermaid, draw.io and Excalidraw import."
---

# Diagram Design

The full skill (instructions, per-diagram-type references, check scripts) lives on GitHub at cathrynlavery/diagram-design, pinned to commit `0cf73c3fcc56667ad91a9a04c439ac6ccfabc9d1`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/diagram-design"; P=skills/diagram-design
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/cathrynlavery/diagram-design 0cf73c3fcc56667ad91a9a04c439ac6ccfabc9d1 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`references/...`, `scripts/...`) resolve against the skill folder, and "this skill's directory" or "the installed skill directory" means the skill folder.
- Run its Python scripts with `python3`.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.