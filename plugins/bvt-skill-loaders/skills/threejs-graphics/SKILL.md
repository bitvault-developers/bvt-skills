---
name: "threejs-graphics"
description: "High-end Three.js visuals: bloom, shadows, ambient occlusion, colour grading, water, clouds, atmosphere, procedural materials, terrain, vegetation, buildings and VFX, plus visual validation. Use to make a 3D scene or game look premium."
---

# Three.js Awesome Graphics

scottstts/Threejs-Awesome-Graphics-Agent-Skills (24 skills) for premium-looking Three.js graphics; its threejs-skill-router skill picks the right ones. It lives on GitHub at scottstts/Threejs-Awesome-Graphics-Agent-Skills, pinned to commit `53eb5a24097425d82532ec33697ad472750132a4`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/threejs-graphics"; P=skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills 53eb5a24097425d82532ec33697ad472750132a4 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/threejs-graphics/skills" "your keywords here" <<'PY'
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
- Start with threejs-skill-router when the task spans several effects.
- Pages must still render on phones, including the iPhone Claude app's WebView: check WebGL capabilities and keep a lower-quality fallback for every heavy effect.
- Ask the user before a skill installs tools (including `curl ... | sh` installers), uses their accounts, deploys, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.