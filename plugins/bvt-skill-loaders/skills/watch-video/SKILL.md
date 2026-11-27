---
name: "watch-video"
description: "Let Claude watch a video from a URL or local file: downloads it, extracts frames, pulls the transcript, and answers questions about what's in it. Use to summarize or analyze a video, reel, lecture or tutorial."
---

# Watch Video

bradautomates/claude-video (MIT) — its `watch` skill downloads a video with yt-dlp, extracts frames with ffmpeg, pulls the transcript from captions (or Whisper), and hands it to Claude to answer questions. Pinned to commit `03ceb42f7fa2c4439aca01752118044baabffb8f`, reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/watch-video"; P=skills/watch
[ -f "$R/$P/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/bradautomates/claude-video 03ceb42f7fa2c4439aca01752118044baabffb8f && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder in full and follow it. In it:
- Relative paths (`references/...`, `scripts/...`) resolve against the skill folder; write absolute paths, since shell variables don't carry between commands.
- ffmpeg is available here; `yt-dlp` installs with `pip install --break-system-packages yt-dlp` if missing. If your environment's network is allowlisted, so downloading from some video sites (e.g. YouTube) may be blocked — when a download is refused, say so and ask the user to attach the file, or use the Gemini-API path the skill describes.
- A local video file the user attaches always works; a URL depends on whether the host is reachable.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.