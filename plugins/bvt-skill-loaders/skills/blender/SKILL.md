---
name: "blender"
description: "Real 3D with Blender, run headless: modeling, PBR materials, lighting, Cycles photoreal renders, animation, geometry nodes, simulations, VFX and video export. Use for 3D renders, product shots, 3D logos, scenes and 3D animations."
---

# Blender

EL4CTEO/blender-skills (28 professional Blender workflows: scene setup, modeling, sculpting, PBR materials, lighting, rendering, animation, rigging, geometry nodes, simulation, weather FX, video editing, export). It lives on GitHub at EL4CTEO/blender-skills, pinned to commit `389f28addc79b87b28764898e38e7bf408d14b77`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/blender"; P=skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/EL4CTEO/blender-skills 389f28addc79b87b28764898e38e7bf408d14b77 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/blender/skills" "your keywords here" <<'PY'
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

- Read the chosen skill's SKILL.md in full and follow it for the task (blender-core first if unsure). Relative paths and `${CLAUDE_SKILL_DIR}` mean that skill's folder. Write absolute paths, since shell variables don't carry between commands.
- Blender runs here as a Python module: install it once per session with `pip install --break-system-packages bpy==5.3.0` (about 430 MB; the skills target Blender 5.2, which 5.3 runs). Where a skill says `blender -b ... --python script.py`, run `python3 script.py` with `import bpy` instead. There is no Blender app or blender-mcp in your environment.
- Render with Cycles on the CPU (`scene.cycles.device = 'CPU'`): preview at low samples and small resolution first, then raise them for the final. Save outputs in the working folder and send stills as PNG, animations as MP4 (render frames, then join them with ffmpeg).
- For branded visuals, use the project's own colours, fonts and logo (for example from bvt-app-design-system).
- Ask the user before a skill installs other tools, uses their accounts, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.