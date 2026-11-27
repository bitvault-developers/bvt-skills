---
name: "impeccable"
description: "Design, critique, audit, polish or improve a frontend interface (sites, dashboards, app UI, forms, iOS/Android screens): hierarchy, layout, type, colour, motion, UX copy, accessibility. Inside a project with a fixed design system it polishes within that look. Not for backend-only work."
---

# Impeccable

The full skill (instructions, reference guides, command-line launcher) lives on GitHub at pbakaus/impeccable, pinned to commit `e89e3ada3e875a89ac2c5d33d11e65ebef6fe285`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/impeccable"; P=.claude/skills/impeccable
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/pbakaus/impeccable e89e3ada3e875a89ac2c5d33d11e65ebef6fe285 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`reference/...`, `scripts/...`) resolve against the skill folder.
- `<skill-base-dir>`, the skill directory and `.claude/skills/impeccable` all mean the skill folder, so `.claude/skills/impeccable/scripts/impeccable` is `<skill folder>/scripts/impeccable`.
- That launcher downloads its engine binary once from the repo's GitHub releases on first run.
- If the project already has a fixed look (for example the bvt-app-design-system and bvt-frontend-system skills), take colours, fonts, tokens and structure from it, and polish, critique or harden within that look instead of choosing a new style.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.