---
name: "hallmark"
description: "Design skill for new websites and pages that look designed, not AI-generated. Use when asked to build or design something new, or when Hallmark is named. Inside a project with a fixed design system it works within that look. Not for existing designs unless Hallmark is named."
---

# Hallmark

The full skill (instructions, layout and theme references, lint scripts) lives on GitHub at Nutlope/hallmark, pinned to commit `4f6a46c6dc325d40ab268c93e25c7b96676ebccd`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/hallmark"; P=skills/hallmark
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/Nutlope/hallmark 4f6a46c6dc325d40ab268c93e25c7b96676ebccd && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`references/...`, `scripts/...`) resolve against the skill folder; its scripts need only Node.
- The skill directory, `SKILL_DIR` and `${CLAUDE_SKILL_DIR}` all mean the skill folder.
- If the project already has a fixed look (for example the bvt-app-design-system and bvt-frontend-system skills), take colours, fonts, tokens and structure from it, and use Hallmark's layout and craft rules inside that look instead of its theme picker.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.