---
name: bvt-ai-translation-qa
description: Uses large language models to translate BitVault strings and reviews the output for quality, glossary adherence and safety before shipping. Use when machine translating a locale, evaluating translation quality, setting up automated localization quality checks, or deciding which content requires a human translator.
---

# AI Translation & QA

## Prompt shape that actually works
Never send a bare string. Every request carries:
1. **The glossary terms present in the string**, with the required target term and forbidden alternatives.
2. **The context/description** and, where possible, the screenshot reference.
3. **The do-not-translate list** (tickers, addresses, product names, units).
4. **The ICU structure**, with an instruction to preserve every argument name and plural category exactly.
5. **Register and audience**: financial UI, plain language, non-promotional; the politeness level for Japanese; everyday Hindi, not officialese.
6. **The length limit**, if the string has one.

Translate a **namespace at a time, not a string at a time** — an LLM's advantage over older MT is cross-string consistency, and per-string calls throw it away.

## Automated checks on every output (before a human sees it)
- **Placeholder integrity**: identical argument set, same names, same count. Fail otherwise.
- **ICU validity**: parses, and every plural category required by the target language is present.
- **Glossary adherence**: score per term; any miss is a fail, not a warning.
- **DNT integrity**: tickers, addresses, product names unchanged, character for character.
- **Length**: within `maxLength`.
- **Round-trip sanity**: back-translate to English and flag large semantic drift for review. Cheap, catches inversions and dropped negations — the failure mode that matters most ("cannot be reversed" → "can be reversed").

## The quality signal to actually track
The **diff between the AI draft and the human post-edit** is the strongest quality measure available, and it is free. Track translation edit rate per language pair and categorize the edits (register, glossary, dropped clause, idiom). A pair with a high edit rate is telling you that pair needs a human first, not that the reviewer is fussy.

## What must never ship AI-only
- The **`security` namespace** — seed warnings, irreversibility, anti-phishing copy.
- **Risk disclosures and any legally required text** (see `bvt-regulatory-translation`).
- Anything in a market you are licensed in, where a regulator reads the local-language version.

These get a qualified human translator plus a second reviewer. The cost is small and the exposure is not.

## Data handling
Do not paste unreleased product copy or anything under NDA into a public MT endpoint. Some free TMS tiers add your translations to a **shared global translation memory** — check the plan terms before enabling machine translation on a free account.

## Honest limits
AI translation is good enough for the bulk of UI copy in high-resource languages and improving fast in mid-resource ones. It is not a substitute for a native reviewer in a market you are launching into, and it does not know that your users read "wallet" one way and your competitor's users read it another. Use it to remove the typing, not the judgement.
