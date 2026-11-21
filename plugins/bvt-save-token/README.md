# BVT SAVE TOKEN

A Claude plugin that helps you use fewer tokens, so your usage limit lasts longer.

## What it does
- **Short replies:** the answer comes first, with no filler.
- **Diff-only code:** you get only the changed lines, not the whole file again.
- **Handoff notes:** a short note (200 words or less) you paste into a new chat, so Claude stops re-reading a long old chat.
- **Setup audit:** tells you which connectors, plugins and skills to turn off.

## Install

```text
/plugin install bvt-save-token --marketplace bitvault-developers/bvt-skills
```

Or download `bvt-save-token.zip` from the [`dist`](../../dist) folder and upload it where you add skills in Claude's settings.

## How to use it
Type one of these in any chat:

| Say this | What happens |
|---|---|
| `BVT SAVE TOKEN on` | Short replies and diff-only code for the rest of the chat |
| `BVT SAVE TOKEN off` | Normal replies again |
| `handoff` | Writes a note to paste into a new chat |
| `audit` | Lists what to turn off to save tokens |

## What to expect
- The biggest savings come from **handoffs** (starting fresh chats) and a **smaller setup** (fewer plugins and connectors switched on).
- Shorter replies save only a little, because most tokens are things Claude re-reads, not words it writes.

## Limits
- It can't change how Anthropic counts usage.
- It can't see a live token meter in chat.
- It can't turn other plugins off for you. You do that in settings.

## Tip
Keep only one copy switched on. If you also have the standalone BVT SAVE TOKEN skill, turn one of them off, because two copies load the same rules twice.

By the BitVault Founding Team · https://bitvault.club
