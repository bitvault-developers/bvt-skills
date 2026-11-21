---
name: bvt-i18n-architecture
description: Sets up and maintains the internationalization architecture for crypto apps across mobile, desktop, web and extension, covering library choice, catalog layout in the monorepo, namespaces, key naming, locale detection and fallback chains. Use when adding a language, restructuring translation files, wiring i18n into a new app shell, or deciding where a string lives.
---

# i18n Architecture

## Library choice
**Default: `i18next` + `react-i18next` + `i18next-icu`.** It is the only option that runs unchanged across all four shells (Expo RN, Tauri desktop webview, PWA, MV3 extension) and it has a native runtime backend for over-the-air translation delivery.

The ICU plugin is not optional. i18next's own plural format uses key suffixes (`key_one`, `key_few`, `key_other`); ICU MessageFormat uses inline syntax. Every serious TMS speaks ICU, and a non-ICU format becomes migration pain later. Standardize on ICU from day one.

Alternative worth knowing: **LinguiJS** — compile-time extraction, smallest runtime (~3KB vs ~8KB+), and `lingui extract` makes a missing translation a **build failure** rather than a runtime surprise. Choose it only if you would rather have build-time guarantees than ecosystem breadth. Do not mix the two.

`react-intl` is strict ICU but heavier and web-leaning. Fine, not better here.

## Where catalogs live
```
packages/i18n/
  src/index.ts            init, detection, fallback
  src/format.ts           number/date wrappers
  locales/
    en/common.json  wallet.json  exchange.json  errors.json  security.json
    hi/…  ar/…  es/…
```
`packages/i18n` is a **pure-TS package** — no react-native, no DOM. Each shell supplies its own locale detector and storage through a port, exactly like the crypto and storage packages.

## Namespaces
Split by domain, not by screen: `common`, `wallet`, `exchange`, `errors`, `security`, `onboarding`. Screens get renamed; domains don't. Lazy-load `exchange` only in the exchange client so the wallet bundle stays small.

## Key naming
`namespace:section.element.state` — e.g. `wallet:send.button.confirm`, `errors:rpc.timeout`.
- Keys are **stable identifiers, never English text**. Renaming a key orphans it in every locale file, silently, forever.
- Never build a key at runtime by concatenation — the extractor cannot see it and the linter cannot check it.
- A key removed from code must be removed from every locale file in the same commit.

## Locale detection and fallback
Order: explicit user choice (persisted) → device locale → `en`.
Fallback chain must be **language-aware, not flat**: `hi-IN → hi → en`, `pt-BR → pt → en`, `ar-EG → ar → en`. A flat fallback to `en` throws away a perfectly good regional variant.

Persist the user's choice outside the translation layer, and re-apply it before first paint — a flash of English on a Hindi device is a trust problem in a finance app.

## Hard rules
- One source of truth: **English is the source language**; no locale file is edited by hand except `en`.
- `en` is complete by definition; CI fails if any key exists in a target locale that is missing from `en` (an orphan) or if `en` gained a key with no `description`.
- Never ship a locale that is below the completeness threshold — a half-Hindi UI is worse than an English one.
