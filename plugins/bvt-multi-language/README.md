# BVT Multi Language

A Claude skill that makes any website or app multilingual: a language switcher, language files, right-to-left support, SEO for every language, translation into as many languages as possible, and a quality check before release.

## Install

```text
/plugin install bvt-multi-language --marketplace bitvault-developers/bvt-skills
```

Or download `bvt-multi-language.zip` from the [`dist`](../../dist) folder and upload it where you add skills in Claude's settings.

## What you get

- **Works on every platform:** plain HTML, React, Next.js, Vue/Nuxt, Svelte, Angular, Flutter, FlutterFlow, React Native/Expo, Android, iOS, Electron, Tauri, WordPress and backends.
- **A proper language switcher:** native language names, search, suggested languages first, no flags, saved choice, correct `lang` and `dir`.
- **Honest quality tiers:** from A (human reviewed) to D (machine only, shown as "beta") and E (community).
- **7 scripts** (Python standard library, plus Node for the registry and Playwright for screenshots):

| Script | What it does |
|---|---|
| `mt_translate.py` | Batch translation with Google, Azure, DeepL, LibreTranslate or Claude. Only new or changed text, cached, placeholders protected, reviewed strings never overwritten, cost estimate first. Claude also writes ICU and the plural forms each language needs. |
| `check_locales.py` | Release gate: missing keys, broken placeholders and ICU, plural forms per language, glossary terms, plus a pseudo-locale for layout tests. |
| `convert_locale_format.py` | Converts JSON, Flutter ARB, gettext PO/POT (WordPress), Android `strings.xml` and iOS `.xcstrings` into each other. |
| `make_registry.mjs` | Builds `languages.json`: native names, script, direction, plural forms, tier and fallback. |
| `find_hardcoded.py` | Finds text still hard-coded in React, Vue, Svelte, Angular, HTML, PHP, Flutter, Android, Kotlin and Swift. |
| `seo_hreflang.py` | Generates hreflang tags and a multilingual sitemap, and checks a built site. |
| `screenshot_langs.py` | Screenshots every language and catches raw keys, unfilled placeholders, wrong `lang`/`dir` and JavaScript errors. |

## Use it

Ask Claude things like:
- "Add a language switcher to this app and make it ready for 100 languages."
- "Translate our app into Hindi, Arabic and Spanish."
- "Check our translations before release."

## Limits

- No translation service covers every language well. Rare languages are labeled "beta" until a native speaker reviews them.
- Paid translation APIs cost money beyond their free tiers. The script always shows the estimate first.
