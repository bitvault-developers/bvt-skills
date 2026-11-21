---
name: bvt-string-authoring
description: Writes source strings for BitVault that survive translation, covering context descriptions, length limits, avoiding concatenation and embedded markup, and the security copy that must not be softened. Use when adding user facing text to any screen, writing error messages, or reviewing English copy before it goes to translators.
---

# Source String Authoring

## The translator sees the string, not the screen
Every key carries:
```json
{ "wallet:send.button.confirm": {
    "message": "Confirm",
    "description": "Primary button on the send-transaction review screen. Irreversibly broadcasts the transaction.",
    "maxLength": 20 } }
```
Without `description`, "Confirm" is ambiguous in most languages (confirm-an-action vs confirm-a-fact vs acknowledge). Without `maxLength`, German and Hindi overflow the button.

Better still: attach a **screenshot** in the TMS. Context beats prose.

## Rules
1. **One message per sentence.** Never assemble from fragments.
2. **No markup in the string.** Use component interpolation.
3. **No runtime key construction.** `t('status.' + s)` is invisible to extraction and lint.
4. **Name arguments meaningfully.** `{amount}` and `{token}`, never `{0}` and `{1}` — a translator reordering positional args gets it wrong.
5. **Never translate an identifier.** Ticker symbols, network names, chain ids, addresses, hashes, derivation paths and units stay literal (see `bvt-crypto-terminology`).
6. **Write for expansion.** Assume the target is 30–40% longer than English; Devanagari is also taller.
7. **No baked-in units or symbols.** Not "Amount in ₹" — pass the currency as an argument so the formatter decides.
8. **No humour, no idiom, no puns** in a finance UI. They do not survive translation and they undermine trust.

## Errors
Error strings are the worst-translated part of most apps because they are written last. Give each one: what happened, what it means for the user's money, and what to do next. Map every provider error to a stable key — never surface a raw RPC string, which is untranslatable by definition.

## Security copy that must not be softened by a translator
Mark these as **locked / review-required** in the TMS:
- the seed phrase is the wallet; anyone with it controls the funds
- BitVault cannot recover it; there is no reset
- no support flow will ever ask for it
- this transaction is irreversible

These are anti-phishing controls, not marketing copy. A translator who softens "irreversible" into "final" has changed the product's risk profile. Require a second reviewer on the `security` namespace.

## Length discipline
Buttons and tab labels get a hard `maxLength`. Balances and addresses get **none** — they are never truncated on a confirmation screen. If a translation cannot fit a button, change the design, not the meaning.
