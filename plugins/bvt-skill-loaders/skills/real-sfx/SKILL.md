---
name: "real-sfx"
description: "Clipwing real-sfx: sound-design motion videos with real recorded sound effects placed on the exact frame, keeping music and voice. Use to add SFX, or to replace synthetic sounds in a video with real ones."
---

# Real SFX (Clipwing)

Clipwing/skills `real-sfx`: finds the moments in a video (from a cue list, a screen recording or the picture), picks real recordings from the user's own sound library, places them on the exact frame at the right level, keeps the music and voice, and returns a new MP4, a separate SFX WAV track, a cue report and a self-critique. It ships 78 UI sounds in 12 styles (the `uisfx` package, MIT); every other sound comes from a library the user adds. Pinned to commit `edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, about 15 MB)

```bash
R="$HOME/.skill-src/real-sfx"; P=skills/real-sfx
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/Clipwing/skills edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder: run its scripts from there, as its SKILL.md says.

## 2. Use it

- Read `SKILL.md` in that folder in full and follow it. Relative paths (`scripts/...`, `references/...`) resolve against the skill folder; write absolute paths, since shell variables don't carry between commands.
- Keep working files in the user's project folder (`work/`, `result/`), never in the skill folder or the user's originals.
- With no sound library added, only the 78 UI sounds are available. To build a library, find sounds with the openverse-sounds skill (or Freesound CC0, Mixkit, Pixabay, Sonniss GDC bundles), then add the folder with `setup.py add-library NAME PATH --index`.
- Ask before its optional installs: `listen.py install --yes` (a private Python environment plus a 16 MB model from Hugging Face) and `setup.py init --uisfx` (npm). In a sandboxed cloud environment the sound hosts are blocked, so libraries live on the user's computer; run it there through a shell on that computer when you have one.
- Use only sounds whose license allows the use (CC0, public domain, CC BY with credit, Mixkit or Pixabay licenses), and list them in the project's CREDITS.
- The Clipwing repo has no license file: use the skill, but don't republish its code.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.