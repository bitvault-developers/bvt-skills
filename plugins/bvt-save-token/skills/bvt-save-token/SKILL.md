---
name: bvt-save-token
description: BVT SAVE TOKEN cuts Claude usage with short replies, diff-only code, chat handoff notes and a setup audit. Use when the user says BVT SAVE TOKEN, save tokens, token saver, handoff, audit, or a chat gets long.
---

# BVT SAVE TOKEN

Goal: give the same quality of answer while using fewer tokens.

Most tokens are input, meaning things Claude re-reads on every message: the whole chat history, files, tool results, and the list of enabled skills and connectors. Shorter chats and smaller reads save the most. Shorter replies help, but only a little.

## Commands the user can say
- "BVT SAVE TOKEN on" (or "token saver on"): follow the Reply rules for the rest of the chat.
- "BVT SAVE TOKEN off" (or "token saver off"): go back to normal replies.
- "handoff": read `references/handoff.md` and write the handoff note.
- "audit": read `references/audit.md` and run the setup audit.

## Reply rules (when on)
1. Give the answer first. Don't restate the question, don't add a preamble, and don't end with offers or a recap of what was just done.
2. Keep prose short. Use at most 5 bullets unless the content really needs more.
3. Code: send only what changed. Use a unified diff, or the full changed function with a one-line location note (for example "in src/app.js, replace fetchPrice()"). Reprint a whole file only if it is new, under about 40 lines, or the user asks. Put all edits in one message.
4. Commands: put them in one code block. Add a comment only on a step that is risky.
5. Never paste back content the user just gave.
6. Explain only when asked. Add no extras nobody asked for.
7. Use images or diagrams only when they explain something faster than words.
8. Never cut safety warnings, errors, or anything the user must act on, even to save tokens.

## Read less (the input side)
- Before reading a file, attachment, connector or web page, decide exactly which piece is needed and fetch only that: a line range, one function, or one search hit, not the whole thing.
- Don't re-read something already read in this chat unless it has changed.
- Prefer one targeted web search over many. Don't start Research unless asked.
- Don't load other skills "just in case".
- If a task is simple (a small edit or a quick lookup), tell the user once, in one line, that a smaller model or lower effort would do. The model can't be changed from inside the chat.

## When to suggest a new chat
Suggest a handoff and a new chat in one line, once, when any of these is true:
- the chat has moved to a different topic or project
- the chat has about 30 or more back-and-forth messages, or several big files or pastes
- earlier details are starting to get lost

Why: every new message makes Claude re-read the whole chat, so a fresh chat with a short note is usually the biggest single saving.

## Limits (say these honestly if asked)
- This skill can't change how Anthropic counts usage, can't see a live token meter in chat, and can't turn off other skills or connectors. The user has to do that.
- Shorter replies save only a little, because output is a small part of usage. Shorter chats and a slimmer setup save the most.
