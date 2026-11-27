---
name: ponytail
description: "Ponytail (DietrichGebert/ponytail): lazy senior dev mode, the smallest change that fully solves the task, plus review, audit, debt and gain skills. Use when the user says ponytail, be lazy, simplest solution, yagni, or complains about over-engineering."
---

# Ponytail

DietrichGebert/ponytail (MIT): one prompt that makes the agent solve the whole problem with the least new code, plus `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain` and `ponytail-help`. Pinned to commit `ebd8654c2c627f721eb8f9c0d1bd4090a29f9e10`, reviewed before publishing (plain SKILL.md files, no scripts). This file only fetches them; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/ponytail"; P=skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/DietrichGebert/ponytail ebd8654c2c627f721eb8f9c0d1bd4090a29f9e10 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
ls "$R/$P"
```

## 2. Use it

- Coding mode: read `$HOME/.skill-src/ponytail/skills/ponytail/SKILL.md` in full and follow it (levels lite, full, ultra).
- Reviewing a change: `skills/ponytail-review/SKILL.md`. Whole-repo audit: `skills/ponytail-audit/SKILL.md`. Tech debt: `skills/ponytail-debt/SKILL.md`. Savings report: `skills/ponytail-gain/SKILL.md`.
- Lazy means less code, never less care: keep validation at trust boundaries, error handling for data loss, security and accessibility.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising the skill from memory.
