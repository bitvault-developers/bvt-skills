---
name: "last30days"
description: "Research what people are saying about any topic in the last 30 days across Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub and the web, then summarize it. Use for last30days or recent-trends requests."
---

# Last 30 Days

The full skill (instructions, references, Python research engine) lives on GitHub at mvanhorn/last30days-skill, pinned to commit `6894d44e088c449ecdd7246a18763fddba1ff805`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/last30days"; P=skills/last30days
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" .claude-plugin && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/mvanhorn/last30days-skill 6894d44e088c449ecdd7246a18763fddba1ff805 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Bind `SKILL_DIR` to the printed skill folder; that is the root SKILL.md for this host. Relative paths (`references/...`, `scripts/...`) resolve against it.
- It needs Python 3.12 or newer; resolve it the way its runtime reference says.
- Reddit, Hacker News, Polymarket, GitHub and web sources work without keys. Set up paid keys (ScrapeCreators, xAI and others) only when the user asks, and tell them first that those calls can cost money.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.