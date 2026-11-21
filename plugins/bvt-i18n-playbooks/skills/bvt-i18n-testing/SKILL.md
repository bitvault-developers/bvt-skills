---
name: bvt-i18n-testing
description: Tests BitVault localization including pseudolocalization, per locale screenshots, missing and hardcoded string detection, right to left smoke tests and on device formatting checks. Use when adding a language, before a release that touches user facing text, or when setting up localization checks in continuous integration.
---

# Localization Testing

## Pseudolocalization — run this every build
Generate a `en-XA` pseudo-locale that: expands each string ~40%, accents every character, and wraps it in brackets.
`Confirm transaction` → `[Ĉöñƒîŕɱ ţŕàñšàçţîöñ————]`

It finds, with zero translation cost:
- **hardcoded strings** — anything rendering unbracketed is not going through `t()`
- **clipped layouts** — anything truncated will break in German or Hindi
- **concatenation** — fragments appear as separate bracketed runs

Add a second pseudo-locale `en-XB` that reverses text and forces RTL to smoke-test mirroring without shipping Arabic.

## CI checks (see also `bvt-translation-pipeline`)
- lint rule banning string literals in JSX
- key present in code but missing from `en` → fail
- orphan keys in targets → fail
- ICU parse + argument-set match across all locales → fail
- completeness threshold per locale, 100% on `security` and `errors`

## Per-locale screenshots
Automate one screenshot per key screen per shipped locale (Maestro or a snapshot runner) and diff them. This is the only reliable way to catch a layout that broke in a language nobody on the team reads. Prioritise: onboarding, seed backup, seed verify, send review, receive, order ticket, settings.

## On-device formatting tests — not in Node
Because Hermes' `Intl` differs from Node's, formatting assertions must run **on a device or emulator**:
- `en-IN` grouping produces `12,34,567`
- INR currency renders `₹` in the right position
- a bigint token amount round-trips to the expected display string
- dates format without throwing in every shipped locale
- plural categories resolve for Arabic (`zero`/`two`/`few`/`many`) and Russian

A `RangeError` from Hermes' number formatter in one locale on one platform is a real, shipped-in-production failure mode. Test for it explicitly.

## RTL smoke test
Per RTL locale: layout mirrors, back arrow flips, coin logos do **not** flip, and — most important — **an address and an amount render in correct order inside RTL text**. Compare the rendered address character by character against the source.

## Manual native review before launching a market
No amount of automation replaces a native speaker walking the send flow, the seed backup flow, and the error states. Budget one review pass per market, not per release.

## Release gate
A locale ships only when: completeness threshold met, `security` at 100% and human-reviewed, screenshots clean, no ICU errors, and on-device formatting tests pass on both platforms.
