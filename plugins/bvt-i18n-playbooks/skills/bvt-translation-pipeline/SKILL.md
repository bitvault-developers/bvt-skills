---
name: bvt-translation-pipeline
description: Runs your translation pipeline from source string to shipped locale, covering translation management system choice, continuous sync, completeness gates in continuous integration, and over the air translation delivery within app store rules. Use when setting up or changing the localization toolchain, adding a language to the pipeline, or shipping a translation fix without a full release.
---

# Translation Pipeline

## Platform choice
| Platform | Fit | Watch out |
|---|---|---|
| **Locize** | i18next-native: `i18next-locize-backend` connects at runtime, CDN delivery, **no redeploy**; missing keys auto-saved | paid per hosted words |
| **Crowdin** | huge integration ecosystem, **mobile OTA SDKs**, generous free tier (~60K hosted words) | free-plan translations may be added to its **global translation memory** — check before putting product copy through it |
| **Tolgee** | open-source, self-hostable, in-context editing, free tier ~500 keys | smaller ecosystem |
| **Weblate** | git-centric, self-host or hosted (~€47/mo) | ops burden if self-hosted |
| **Lokalise** | best editor UX, strong mobile/Figma workflow | repriced upward in late 2025; expensive for a small team |

**Default for this stack: Locize** (i18next-native, runtime CDN) or **Tolgee self-hosted** if you want the data in-house. Both avoid a redeploy for a wording fix.

## Continuous sync
```
dev writes en/*.json  →  CI pushes source to TMS  →  MT/AI pre-translate
   →  human review     →  CI pulls targets        →  commit
```
- **English is the only locale edited by hand.** Everything else is pulled.
- The TMS is authoritative for targets; the repo is authoritative for source. Never hand-edit `hi/wallet.json` — the next pull overwrites it.
- Branch-aware sync so a feature branch's new keys do not pollute the production catalog.

## CI gates (fail the build)
1. Any key in code with no entry in `en`.
2. Any `en` key with no `description`.
3. Any orphan key present in a target but absent from `en`.
4. ICU syntax validation on every message in every locale — a malformed plural in Arabic throws at runtime, in production, in a locale you do not read.
5. Argument-set mismatch: a target using `{amount}` where the source has `{value}` is a runtime failure.
6. Completeness threshold per shipped locale (e.g. 95% for `security` and `errors` namespaces at 100%).

## Over-the-air translation updates
Two mechanisms, different rules:
- **EAS Update** ships changed JSON as part of a JS/asset update. This is the simplest path and it is within policy — it changes strings, not reviewed behaviour.
- **TMS OTA SDK** (Crowdin-style) fetches translations at runtime from a CDN. Also fine, and it decouples wording fixes from releases entirely.

**Either way: a translation update may correct wording. It may not introduce new functionality, change what an action does, or alter a legal disclosure that was reviewed.** Wording fixes are exactly the case OTA exists for — app review cycles are too slow for a mistranslated button in a finance app.

Cache the last-known-good catalog on device and fall back to the bundled one; a CDN outage must never leave the app showing raw keys.

## Ownership
One person owns the glossary and the `security` namespace review. Everything else can be pipeline-driven.
