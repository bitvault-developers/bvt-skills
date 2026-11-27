---
name: "scrapling"
description: "Web scraping with the Scrapling Python library: fetch pages, parse with adaptive selectors, run sessions and spiders for research data. Use when the user wants to scrape a site or names Scrapling."
---

# Scrapling

The full skill (instructions, references, examples) lives on GitHub at D4Vinci/Scrapling, pinned to commit `95cf9019ab5a5d6f3e9654b7ef1c6a26e29dc5c0`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/scrapling"; P=agent-skill/Scrapling-Skill
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/D4Vinci/Scrapling 95cf9019ab5a5d6f3e9654b7ef1c6a26e29dc5c0 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths (`references/...`, `examples/...`) resolve against the skill folder.
- Install the library when first needed: `pip install --break-system-packages "scrapling[all]>=0.5"` (drop the flag where pip doesn't require it). Browser fetching also needs `scrapling install` once.
- Start with the plain fetchers. Use browser or stealth modes only for sites the user is allowed to access, and respect the site's terms and rate limits.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.