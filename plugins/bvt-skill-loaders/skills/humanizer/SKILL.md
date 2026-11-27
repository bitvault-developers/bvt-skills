---
name: "humanizer"
description: "Rewrite AI-sounding text so it reads like a person wrote it, without changing what it says. Use when editing or reviewing prose for AI tells, or when the user says humanize."
---

# Humanizer

The full skill lives on GitHub at blader/humanizer, pinned to commit `0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/humanizer"
[ -f "$R/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" fetch -q --depth 1 https://github.com/blader/humanizer 0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.