# BVT i18n Playbooks

Fifteen localization skills from the BitVault team for shipping a crypto app in many languages without breaking layouts, numbers or security copy.

| Skill | What it covers |
|---|---|
| `bvt-ai-translation-qa` | Uses large language models to translate BitVault strings and reviews the output for quality, glossary adherence and safety before shipping. |
| `bvt-crypto-terminology` | Maintains BitVault's translation glossary and do not translate list for crypto terminology across all supported languages. |
| `bvt-datetime-i18n` | Formats dates, times and relative times per locale in BitVault apps, covering time zones, exchange timestamps, candle labels and calendar systems. |
| `bvt-fonts-and-scripts` | Selects, loads and tests fonts for the scripts BitVault supports including Devanagari, Arabic, and CJK, covering complex script shaping, fallback chains, bundle size and tabular figures. |
| `bvt-i18n-architecture` | Sets up and maintains the internationalization architecture for BitVault apps across mobile, desktop, web and extension, covering library choice, catalog layout in the monorepo, namespaces, key naming, locale detection and fallback chains. |
| `bvt-i18n-testing` | Tests BitVault localization including pseudolocalization, per locale screenshots, missing and hardcoded string detection, right to left smoke tests and on device formatting checks. |
| `bvt-icu-message-format` | Writes ICU MessageFormat strings for BitVault including plurals, select, gender, nested arguments, interpolation and escaping. |
| `bvt-number-currency-i18n` | Formats numbers, token amounts and fiat currency correctly per locale in BitVault apps, covering the Intl API, Hermes gaps on React Native, Indian lakh and crore grouping, native digit systems and bigint token amounts. |
| `bvt-regulatory-translation` | Handles translation of BitVault legal, risk and regulatory content including white papers, disclosures and terms across jurisdictions. |
| `bvt-rtl-layout` | Implements right to left layout for Arabic, Hebrew, Farsi and Urdu across BitVault mobile, desktop, web and extension shells, covering layout mirroring, icon flipping, bidirectional text isolation and the restart requirement. |
| `bvt-seed-phrase-i18n` | Governs language handling for BIP-39 seed phrases in BitVault wallets. |
| `bvt-store-listing-i18n` | Localizes BitVault app store listings and metadata for the App Store and Google Play, covering supported metadata languages, locale inheritance, keyword research per market and localized screenshots. |
| `bvt-string-authoring` | Writes source strings for BitVault that survive translation, covering context descriptions, length limits, avoiding concatenation and embedded markup, and the security copy that must not be softened. |
| `bvt-text-expansion-layout` | Designs BitVault interfaces that survive text expansion and script height differences across languages. |
| `bvt-translation-pipeline` | Runs BitVault's translation pipeline from source string to shipped locale, covering translation management system choice, continuous sync, completeness gates in continuous integration, and over the air translation delivery within app store rules. |

These are the playbooks the BitVault team uses for its own apps, so examples name BitVault's tokens and chains (BVT, BRUSD, BRINR, the BVM L2). The rules apply to any similar project.

## Install

```text
/plugin install bvt-i18n-playbooks --marketplace bitvault-developers/bvt-skills
```

Or, in your terminal:

```bash
claude plugin install bvt-i18n-playbooks --marketplace bitvault-developers/bvt-skills
```

For the Claude app, download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.
