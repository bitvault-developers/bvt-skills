---
name: "playwright-browser"
description: "Browser automation with Playwright: test websites and web apps, fill forms, log in, take screenshots, check responsive layouts and links, and script repeatable browser tasks. Use when the user wants to test a site or automate a browser."
---

# Playwright Browser Automation

lackeyjb/playwright-skill, a general-purpose Playwright automation skill. It lives on GitHub at lackeyjb/playwright-skill, pinned to commit `dd47a6a023e249eb1b36e9e943eab89d0900865d`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/playwright-browser"; P=skills/playwright-skill
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/lackeyjb/playwright-skill dd47a6a023e249eb1b36e9e943eab89d0900865d && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/playwright-browser/skills/playwright-skill" "your keywords here" <<'PY'
import sys, re, pathlib
root = pathlib.Path(sys.argv[1]); words = [w for w in re.split(r"\W+", " ".join(sys.argv[2:]).lower()) if len(w) > 2]
rows = []
for p in sorted(root.glob("**/SKILL.md")):
    t = p.read_text(errors="ignore")[:4000]
    n = re.search(r"^name:\s*[\"']?([^\"'\n]+)", t, re.M); name = n.group(1).strip() if n else p.parent.name
    d = re.search(r"^description:\s*[>|]?\s*(.*?)(?=^[\w-]+:|^---)", t, re.S | re.M)
    desc = " ".join((d.group(1) if d else "").split()).strip("\"'")[:200]
    score = sum(f"{name} {desc}".lower().count(w) for w in words)
    if score or not words: rows.append((-score, name, desc, str(p)))
for _, n, d, p in sorted(rows)[:15 if words else None]: print(f"- {n} — {d}\n  {p}")
PY
```

## 3. Use it

- Read the chosen skill's SKILL.md in full and follow it for the task. Use two skills only when the task clearly needs both.
- Relative paths (`references/...`, `scripts/...`, `rules/...`) resolve against that skill's folder; `SKILL_DIR`, `${CLAUDE_SKILL_DIR}` and "this skill's directory" mean that folder, and `${CLAUDE_PLUGIN_ROOT}` means the folder two levels above it. Write absolute paths, since shell variables don't carry between commands.
- Playwright and Chromium are preinstalled in your environment: if `node -e "require('playwright')"` works, skip its `npm run setup` instead of installing them again.
- Automate only sites the user owns or is allowed to automate, follow the site's terms, and never try to defeat CAPTCHAs or bot checks.
- Ask the user before a skill installs tools (including `curl ... | sh` installers), uses their accounts, deploys, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.