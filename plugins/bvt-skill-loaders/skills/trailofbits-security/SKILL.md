---
name: "trailofbits-security"
description: "Trail of Bits security skills: smart contract and token integration review, audit prep, code maturity, secure workflows, Semgrep/CodeQL, fuzzing, property testing, supply-chain risk, and bug triage. Use for security reviews and audits."
---

# Trail of Bits Security

Trail of Bits' collection (98 security skills), including its building-secure-contracts set for smart contracts. It lives on GitHub at trailofbits/skills, pinned to commit `e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/trailofbits-security"; P=plugins
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/trailofbits/skills e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/trailofbits-security/plugins" "your keywords here" <<'PY'
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

- Read the chosen skill's SKILL.md in full and follow it for the task. Use two skills only when the task clearly needs both.
- Relative paths (`references/...`, `scripts/...`, `rules/...`) resolve against that skill's folder; `SKILL_DIR`, `${CLAUDE_SKILL_DIR}` and "this skill's directory" mean that folder, and `${CLAUDE_PLUGIN_ROOT}` means the folder two levels above it. Write absolute paths, since shell variables don't carry between commands.
- For smart contracts start with the building-secure-contracts skills (token-integration-analyzer, secure-workflow-guide, guidelines-advisor, audit-prep-assistant, code-maturity-assessor).
- Ask the user before a skill installs tools (including `curl ... | sh` installers), uses their accounts, deploys, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.