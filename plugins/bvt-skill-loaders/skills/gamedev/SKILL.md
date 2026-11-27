---
name: "gamedev"
description: "79 game-dev skills plus a router (gamedev-skills/awesome-gamedev-agent-skills): Godot, Unity, Unreal, Roblox, three.js, Phaser and more. Use to make, fix or ship any game, in any engine."
---

# Game dev (awesome-gamedev-agent-skills)

gamedev-skills/awesome-gamedev-agent-skills (Apache-2.0): 79 skills for 12 engines (Godot, Unity, Unreal, Ebitengine, Bevy, Phaser, PixiJS, three.js, Defold, LÖVE, pygame, Roblox), plus disciplines (game feel, camera, UI, audio, AI, shaders, save systems, procedural generation, level design, assets), genres (platformer, RPG, roguelike, tower defense, card game, FPS and more) and shipping workflows (Steam, itch.io, game jams). A router picks the few skills a task needs. Pinned to commit `c6ca6c41c839b68319ffc08430b99ab768debc32`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md files.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/gamedev"
[ -f "$R/router/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set router skills && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/gamedev-skills/awesome-gamedev-agent-skills c6ca6c41c839b68319ffc08430b99ab768debc32 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R" && pwd
```

The printed path is the library root.

## 2. Use it

- Read `$HOME/.skill-src/gamedev/router/SKILL.md` in full and follow it. Its `skills/...` paths resolve against the library root; its `references/...` paths resolve against the `router` folder. Then read only the skills it picks, and their `references/` files only when needed.
- Write absolute paths, since shell variables don't carry between commands.
- Game engines (Godot, Unity, Unreal, Roblox Studio and the others) are not installed in a sandboxed cloud environment. Web games (three.js, Phaser, PixiJS) and pygame can be built and tested here; for other engines, write the project files here and say which steps need the engine on the user's computer. Ask before installing an engine or system software.
- Ask before publishing anything (Steam, itch.io, a store) or using the user's accounts or secrets.
- Use the project's own names and look, and never other brands' characters or logos.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skills from memory.