---
name: "task-observer"
description: "Notes user corrections, judgement calls and repeated workflows during multi-step work, then turns them into skill improvements or new-skill ideas. Use in longer work sessions, and when the user asks to review a session, log a correction or improve a skill."
---

# Task Observer (One Skill to Rule Them All)

The full skill (instructions, references, helper scripts) lives on GitHub at rebelytics/one-skill-to-rule-them-all by Eoghan Henn and contributors (CC BY 4.0), pinned to commit `046b8f2aa6bdae369a93ae563889b7cc449d17ad`, which was reviewed before install. This file only fetches it; the real instructions are in the fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/task-observer"
[ -f "$R/SKILL.md" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" fetch -q --depth 1 https://github.com/rebelytics/one-skill-to-rule-them-all 046b8f2aa6bdae369a93ae563889b7cc449d17ad && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R" && pwd
```

The printed path is the skill folder.

## 2. Use it

Read `SKILL.md` in that folder and follow it as this skill's instructions. In it:
- Relative paths (`references/...`, `scripts/...`) resolve against the skill folder.
- Your environment's files reset between sessions, so run in its handoff-doc mode (`references/environments.md`): keep observations during the session and give the user the handoff at the end, not a log on disk.
- Saved skill files here are read-only. Offer each proposed skill change or new skill to the user as a skill save card (the propose_skills tool) instead of editing files.
- Keep it light: it should not slow down or interrupt the user's actual task, and it never changes a skill without the user saving the card.
- Shell variables don't carry between commands, so write the absolute path each time.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.