---
name: "gsap"
description: "GreenSock's official GSAP skills: core tweens, timelines, ScrollTrigger scroll animations, plugins, React and framework use, and performance. Use for premium web and app animation, scroll effects and motion design in code."
---

# GSAP

GreenSock's official skill collection (8 skills: core, timeline, ScrollTrigger, plugins, utils, React, frameworks, performance). It lives on GitHub at greensock/gsap-skills, pinned to commit `aed9cfd3277740755f6bfc1155c7aa645403b760`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/gsap"; P=skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/greensock/gsap-skills aed9cfd3277740755f6bfc1155c7aa645403b760 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/gsap/skills" "your keywords here" <<'PY'
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

- Read the chosen skill's SKILL.md in full and follow it for the task. Relative paths mean that skill's folder. Write absolute paths, since shell variables don't carry between commands.
- If the project has its own design system skill (for example bvt-frontend-system and bvt-app-design-system), it sets the structure and look: animate within it, and where they disagree, follow the design system and say so.
- Keep animation smooth on phones and respect `prefers-reduced-motion`.
- Ask the user before a skill installs tools, uses their accounts, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.