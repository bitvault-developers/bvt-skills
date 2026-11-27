---
name: "langchain"
description: "LangChain's official skills for building AI agents: LangChain and LangGraph fundamentals, RAG, middleware, persistence and memory, Deep Agents, and Python or TypeScript quickstarts. Use when building an LLM agent or AI assistant backend."
---

# LangChain

LangChain's official skill collection for building agents with LangChain, LangGraph and Deep Agents. It lives on GitHub at langchain-ai/langchain-skills, pinned to commit `126c384d8552dcb476b226c244172186cc3f4328`, which was reviewed before install. This file only fetches the collection and picks the right skill from it; the real instructions are in each fetched SKILL.md.

## 1. Fetch it (once per session, a few seconds)

```bash
R="$HOME/.skill-src/langchain"; P=config/skills
[ -d "$R/$P" ] || { rm -rf "$R" && git init -q "$R" && git -C "$R" sparse-checkout set "$P" && git -C "$R" fetch -q --depth 1 --filter=blob:none https://github.com/langchain-ai/langchain-skills 126c384d8552dcb476b226c244172186cc3f4328 && git -C "$R" -c advice.detachedHead=false checkout -q FETCH_HEAD; }
cd "$R/$P" && pwd
```

## 2. Find the right skill

List the collection, or pass a few keywords from the task to rank it:

```bash
python3 - "$HOME/.skill-src/langchain/config/skills" "your keywords here" <<'PY'
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
- Ask the user before a skill installs tools (including `curl ... | sh` installers), uses their accounts, deploys, or changes anything outside the working folder.

Fetch the pinned commit only; never switch to a newer upstream version unless the user asks. If the fetch fails, say so and stop instead of improvising a skill from memory.