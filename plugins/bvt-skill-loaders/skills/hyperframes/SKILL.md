---
name: "hyperframes"
description: "HeyGen's HyperFrames: write HTML, render frame-exact video. Motion graphics, 3D-style title and camera-orbit blocks, captions, slideshows and website-to-video. Use to make animated videos, reels, promos and motion graphics."
---

# HyperFrames

HeyGen's HyperFrames skill collection (9 skills: hyperframes, CLI, block registry, media, slideshow, style sampling, website and video reverse-engineering). It lives on GitHub at heygen-com/hyperframes (Apache 2.0), pinned to commit `be67089a80b59be945d84e09d400a4ece254daef`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/hyperframes"; P=skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/heygen-com/hyperframes be67089a80b59be945d84e09d400a4ece254daef && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/hyperframes/skills" "your keywords here" <<'PY'
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

- Read the chosen skill's SKILL.md in full and follow it for the task (hyperframes first). Relative paths mean that skill's folder. Write absolute paths, since shell variables don't carry between commands.
- Run the CLI pinned and with telemetry off: `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx -y hyperframes@0.9.41 <command>` in place of `npx hyperframes <command>`. Skip the skill's usage-beacon step (`hyperframes events`), and treat plan usage as unknown unless the user has signed in.
- Ask the user before signing in to a HeyGen account, using any cloud or paid feature, installing other tools, or changing anything outside the working folder.
- For branded videos, use the project's own colours, fonts and logo (for example from bvt-app-design-system).

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.