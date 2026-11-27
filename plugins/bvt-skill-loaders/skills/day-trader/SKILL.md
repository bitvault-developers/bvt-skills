---
name: "day-trader"
description: "11 day-trading skills (stock analysis, scanner, news, risk sizing, entry/exit timing, alerts, congressional-trade tracker, broker order executor). Free Yahoo/SEC data, no API key for analysis. Use for stock trading research and setups. Educational, not investment advice."
---

# Day Trader

Jakeschincariol/day-trader-skill (11 skills) for day-trading research on free public data. It lives on GitHub at Jakeschincariol/day-trader-skill, pinned to commit `3d0f4ef6986f4984b7c6bd46f7ff4f87744c3abd`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/day-trader"
[ -f "$R/trader-scanner/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" fetch -q --depth 1 https://github.com/Jakeschincariol/day-trader-skill 3d0f4ef6986f4984b7c6bd46f7ff4f87744c3abd && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/day-trader" "your keywords here" <<'PY'
import sys, re, pathlib
root = pathlib.Path(sys.argv[1]); words = [w for w in re.split(r"\W+", " ".join(sys.argv[2:]).lower()) if len(w) > 2]
rows = []
for p in sorted(root.glob("*/SKILL.md")):
    t = p.read_text(errors="ignore")[:4000]
    nm = re.search(r"^name:\s*[\"']?([^\"'\n]+)", t, re.M); name = nm.group(1).strip() if nm else p.parent.name
    d = re.search(r"^description:\s*[>|]?\s*(.*?)(?=^[\w-]+:|^---)", t, re.S | re.M)
    desc = " ".join((d.group(1) if d else "").split()).strip("\"'")[:200]
    score = sum(f"{name} {desc}".lower().count(w) for w in words)
    if score or not words: rows.append((-score, name, desc, str(p)))
for _, n, d, p in sorted(rows)[:15 if words else None]: print(f"- {n} — {d}\n  {p}")
PY
```

## 3. Use it

- Read the chosen skill's SKILL.md in full and follow it for the task. Relative paths and `${CLAUDE_SKILL_DIR}` mean that skill's folder; run its scripts with `python3`. Write absolute paths, since shell variables don't carry between commands.
- The analysis skills (scanner, analyst, news, risk, entry, exit, alerts, pelosi, timemachine, budget) use free Yahoo/SEC data and need no keys.
- This is market research and education, not investment advice: present data and setups neutrally, never tell the user to buy, sell or hold, and keep the skill's own risk limits.
- trader-broker places real orders through the user's own Alpaca/IBKR account. Keep its defaults: paper trading unless the user sets live, keys only in env/config files (never in chat), and one explicit per-order confirmation before anything is sent. Never place, size or close a live position without the user's yes for that specific order. Ask the user before setting up any broker connection.
- Ask the user before a skill installs tools, uses their accounts, spends money, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.