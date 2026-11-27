---
name: "earshot"
description: "Add real, licensed sound to code-made videos and animations: cue lists, SFX/foley/ambience, music edited to picture, a deterministic mixer, loudness/sync QA and the final mux. Use when a video, reel or animation needs sound design, SFX or a soundtrack."
---

# Earshot

Leonxlnx/earshot (MIT) gives a coding agent ears and sound: a `real-sound` skill that scores a video from real licensed recordings, and an `earshot` skill that lets the agent listen back and review audio. Pinned to commit `4ac3d2ac2b151e1c23376f9ce7f3047a17050013`, reviewed before install. This file only fetches the collection and picks the right skill; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/earshot"; P=skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/Leonxlnx/earshot 4ac3d2ac2b151e1c23376f9ce7f3047a17050013 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

```bash
python3 - "$HOME/.skill-src/earshot/skills" "your keywords here" <<'PY'
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

- Read the chosen skill's SKILL.md in full and follow it. Relative paths (`references/...`, `scripts/...`) resolve against that skill's folder; write absolute paths, since shell variables don't carry between commands.
- It sources audio from Freesound / Mixkit / composer libraries: keep every clip's licence and credit, and only use clips whose licence allows the use.
- Ask the user before a skill installs tools, uses their accounts, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.