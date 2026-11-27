---
name: "ui-ux-pro-max"
description: "UI/UX design intelligence for web, mobile and desktop: styles, palettes, font pairings, UX rules, charts and stack-specific guidance. Use when designing, building, reviewing or fixing any interface. A project's own design system comes first."
---

# UI UX Pro Max

The full skill (instructions, searchable design data, scripts) lives on GitHub at nextlevelbuilder/ui-ux-pro-max-skill, pinned to commit `3a13158ff1f32156cbe144108de48eda2ecaed9a`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/ui-ux-pro-max"; P=.claude/skills/ui-ux-pro-max
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/nextlevelbuilder/ui-ux-pro-max-skill 3a13158ff1f32156cbe144108de48eda2ecaed9a && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`references/...`, `scripts/...`, `data/...`) resolve against the skill folder.
- `${CLAUDE_PLUGIN_ROOT}` means `$HOME/.skill-src/ui-ux-pro-max`, so its `search.py` commands work as written once that variable is set or the path is written out.
- Use `python3` where it says `python` if `python` is missing.
- If the project already has a fixed look (for example the bvt-app-design-system and bvt-frontend-system skills), take colours, fonts, tokens and structure from it, and use this skill's UX rules, chart guidance and stack advice inside that look; skip its palette and font suggestions there.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.