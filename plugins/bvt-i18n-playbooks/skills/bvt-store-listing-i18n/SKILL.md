---
name: bvt-store-listing-i18n
description: Localizes crypto app store listings and metadata for the App Store and Google Play, covering supported metadata languages, locale inheritance, keyword research per market and localized screenshots. Use when preparing a store listing for a new market, translating app metadata, or planning app store optimization across languages.
---

# Store Listing Localization

## What each store supports
- **App Store Connect: 50 metadata languages** (expanded in March 2026 with Bangla, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Slovenian, Tamil, Telugu and Urdu — a meaningful expansion for the Indian market). Localize name, subtitle, description, keywords, promotional text and **screenshots**.
- **Google Play Console: 80+ listing translations**, with store listing experiments and custom listings per country.

Confirm the current list in each console before planning — both stores add languages without much notice.

## App Store locale inheritance — use it
Add one variant and related locales inherit it automatically:
`en-US ↔ en-GB ↔ en-AU ↔ en-CA` · `pt-PT ↔ pt-BR` · `fr-FR ↔ fr-CA` · `es-ES ↔ es-MX ↔ Catalan`.
So localizing `en-GB` and `es-MX` covers more storefronts than the count suggests. Some locales (en-CA, fr-CA, Catalan) cannot be added directly at all and are served from their parent.

## Keywords are researched, not translated
The App Store indexes metadata **per country**. Translating your English keyword list produces terms nobody searches. Research the actual local query for each market — in India that often means the **English or transliterated term** ("crypto wallet") outranks the Hindi calque, because that is what people type.

Cross-localization: for a given country the store may index both the primary and a secondary language's keywords. Use both fields rather than duplicating.

## Screenshots
Localize them. A store page in Hindi with English screenshots converts badly and signals an unlocalized app. Requirements:
- screenshot sizes must match your primary language's set, or a primary-language change is blocked later
- device frames and captions translated; captions are where the expansion budget bites
- show localized **in-app** UI, not translated captions over English screens

## Consistency with the app
Users bounce when the store page is in their language and the app opens in English. **Do not localize a store listing for a market the app itself does not support.** Ship the in-app locale first, the listing second.

## Crypto-specific listing constraints
Store copy must not overstate: no yield promises, no "guaranteed", no price projections, and the same risk framing in every language. Apple's crypto rules and Google's financial-features declarations apply to the **localized** listing too — a claim that is fine in English and stronger in translation is a rejection risk, and a regulator in that market reads the local version.

Keep the do-not-translate list in force: ticker symbols, the brand name and product names are identifiers in every listing.

## Support content
Localize at minimum: the seed-phrase backup article, the recovery article, and the "we will never ask for your seed phrase" notice. These carry the anti-phishing load in-market.
