---
name: "opuscar"
description: "Lemo-Opuscar (the OPUSCAR 98 reel): 99 code-made film styles. Direct, draw, score and mix a short film in a named style: oil paint, ukiyo-e, neon, hologram HUD, glass product, data explainer, newsreel, teardown and more. Use for a styled video, promo or explainer."
---

# Opuscar (Lemo-Opuscar film styles)

The style library, guides and render tools live on GitHub at lemomo-ai/lemo-opuscar (code MIT; guides CC BY-NC 4.0; films you make are yours, commercial use included). It is pinned to commit `3a7132b996be0241c1ea0ab180d519f06e6f10b6`, which was reviewed before install. This file fetches that version and hands over to the library's own skill.

## 1. Fetch the library (once per session, about 18 MB)

```bash
L="$HOME/lemo-opuscar"; SHA=3a7132b996be0241c1ea0ab180d519f06e6f10b6
[ -f "$L/AGENTS.md" ] || { rm -rf "$L" && git init -q "$L" && git -C "$L" remote add origin https://github.com/lemomo-ai/lemo-opuscar.git && git -C "$L" config remote.origin.promisor true && git -C "$L" config remote.origin.partialclonefilter blob:none && git -C "$L" sparse-checkout set --no-cone '/*' '!/styles/*/demo/' '!/styleboard/' '!/docs/readme/' '!/docs/cover.jpg' '!/styles/*/poster.jpg' && git -C "$L" fetch -q --depth 1 --filter=blob:none origin "$SHA" && git -C "$L" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
git -C "$L" rev-parse HEAD
```

## 2. Hand over to the library's skill

Read `$HOME/lemo-opuscar/plugin/skills/lemo-opuscar/SKILL.md` in full and follow it. Its "skill base directory" is `$HOME/lemo-opuscar/plugin/skills/lemo-opuscar`, and its library (`$LIB`) is `$HOME/lemo-opuscar`. Then follow `$LIB/AGENTS.md` as it says.

In a sandboxed environment:
- Run its setup as `LEMO_OPUSCAR_HOME="$HOME/lemo-opuscar" sh "$HOME/lemo-opuscar/plugin/skills/lemo-opuscar/scripts/setup.sh"` (add `deps`, `deps voice` or `demo <slug>` as its guide says). This clone is not marked as managed, so setup uses the pinned version as it is and does not pull newer code. Never update to upstream main unless the user asks.
- For rendering, point Playwright at the browser already installed here when one exists: `export PLAYWRIGHT_CHROME="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux64/chrome 2>/dev/null | tail -1)"` (leave it unset if empty, and let `setup.sh deps` install its browser).
- Narration: prefer the offline Kokoro voice. edge-tts sends the script text to Microsoft's online service, so ask before using it. Styles marked ✦ need an image generator the user provides; ask first.
- Clawd, the orange character in OPUSCAR 98, belongs to Anthropic and is not licensed by the library; never put Clawd or other brands' logos and product UIs in the user's films.
- For brand films, use the brand's own names and branding inside the chosen style.
- Shell variables don't carry between commands, so write absolute paths each time. Ask before installing system software, using the user's accounts, or changing anything outside the working folder.

If the fetch fails, say so and stop instead of improvising the library from memory.