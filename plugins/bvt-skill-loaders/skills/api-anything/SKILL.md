---
name: "api-anything"
description: "Get data from a website through its own underlying requests instead of a browser: a shared catalog of ~114 sites (Reddit, YouTube, GitHub, Google Flights, Goodreads, Amazon…) plus learning a missing read in one call. Use to pull data from a site or turn one into a callable API."
---

# API Anything

goodnight000/api-anything, a skill that reads data from a website through the site's own requests. It lives on GitHub at goodnight000/api-anything, pinned to commit `9641e54aed7e7603e4886891d576e1762a310b11`, which was reviewed before install. This file only fetches the skill; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/api-anything"; P=skills/api-anything
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/goodnight000/api-anything 9641e54aed7e7603e4886891d576e1762a310b11 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it as this skill's instructions. In it:
- Relative paths resolve against the skill folder.
- It runs through the `api-anything` npm package. Pin the version: run `npx -y api-anything@0.4.0` in place of a bare `npx -y api-anything`, so the reviewed version is used.
- Prefer the bundled read catalog. It does no CAPTCHA solving, keeps secrets on the machine, and ships no write operations; keep those defaults.
- Only pull data from sites the user is allowed to, follow each site's terms (the skill says you are responsible for use), and don't sign in to or scrape anyone's private data.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.