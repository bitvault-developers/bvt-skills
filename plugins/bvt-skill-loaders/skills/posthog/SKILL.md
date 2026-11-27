---
name: "posthog"
description: "PostHog's official skills (350+): product analytics, funnels, session replays, error tracking, feature flags, experiments, dashboards and adding PostHog to an app. Use for any PostHog task."
---

# PostHog

PostHog/skills (MIT): PostHog's own skill collection: `skills/posthog` (integration, product analytics, feature flags, error tracking, LLM analytics, logs, migrations, cost cutting) and `skills/omnibus` (about 200 task skills: funnel drop-off, finding sessions to watch, investigating a replay, debugging experiments, building dashboards, alerts, data warehouse). PostHog's internal staff tools in `skills/team` are deliberately not fetched. Pinned to commit `7dcf60cbc79ee9f087c5d958b232a90ea41191d7`, reviewed before install. This file only fetches the collection and picks the right skill; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, about 40 MB)

```bash
R="$HOME/.skill-src/posthog"
[ -d "$R/skills/posthog" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set skills/posthog skills/omnibus && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/PostHog/skills 7dcf60cbc79ee9f087c5d958b232a90ea41191d7 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/skills" && pwd
```

## 2. Find the right skill

```bash
python3 - "$HOME/.skill-src/posthog/skills" "your keywords here" <<'PY'
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

- Read the chosen SKILL.md in full and follow it. Relative paths (`references/`, `scripts/`) resolve against that skill's folder; write absolute paths.
- The skills act on PostHog through the **PostHog connector** (`mcp__PostHog__exec`, plus `render-ui` to show results). If it is not connected, say so and suggest connecting it; do not ask for a personal API key in chat.
- The PostHog connector can also serve skills itself; if it offers one with the same name, either copy is fine, but don't run both.
- Read-only by default. Ask before anything that changes the project: creating, editing or deleting feature flags, experiments, surveys, dashboards, alerts, cohorts, workflows or data sources, and before sending any message or email through PostHog.
- For adding PostHog to an app, use the `skills/posthog/integration` skills. Keep the project key in environment config, mask inputs in session recordings (passwords, seed phrases, wallet addresses, card fields), and never record pages that show secrets.
- Recordings, events and person properties can hold users' personal data: summarize patterns rather than copying personal details into answers or files.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.