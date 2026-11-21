---
name: "bvt-multi-language"
description: "BVT Multi Language Skill. Adds a language switcher and full multilingual system to any website, web app, mobile or desktop app, WordPress, Flutter or FlutterFlow project, translates it into as many languages as possible and checks quality before release. Use when building any digital product, or when languages, translation, multilingual, i18n, localization, locale, RTL or a language switcher come up."
---

# BVT Multi Language Skill

Every product built with this skill ships with a language switcher and is ready for hundreds of languages, even if it launches in one.

Files in this skill:
- `references/platform-recipes.md`: setup code for each platform (web, React, Next.js, Vue, Svelte, Angular, Flutter, FlutterFlow, React Native, Android, iOS, Electron, Tauri, WordPress, backend) and a ready language switcher component.
- `references/translating.md`: translation engines, language coverage, the batch script, Claude translation rules, live translation of user content, cost and legal rules.
- `references/quality-checks.md`: release gate, QA script, review workflow, legal checklist.
- `scripts/mt_translate.py`: batch machine translation (diff-only, cached, placeholder-safe, never overwrites reviewed strings).
- `scripts/check_locales.py`: validates locale files (keys, placeholders, ICU, plural forms per language) and builds a pseudo-locale for layout tests.
- `scripts/convert_locale_format.py`: converts JSON, Flutter ARB, gettext PO/POT (WordPress), Android `strings.xml` and iOS `.xcstrings` into each other.
- `scripts/make_registry.mjs`: builds `languages.json` (native names, script, direction, plural forms, tier, fallback). Run with Node.
- `scripts/find_hardcoded.py`: finds text that is still hard-coded in React, Vue, Svelte, Angular, HTML, PHP, Flutter, Android, Kotlin and Swift files.
- `scripts/seo_hreflang.py`: generates hreflang tags and a multilingual sitemap, and checks a built site.
- `scripts/screenshot_langs.py`: opens the app in every language, takes screenshots and catches raw keys, unfilled placeholders, wrong `lang`/`dir` and JS errors (needs Playwright).
- `assets/glossary.template.csv` and `assets/languages.example.json`: starting points for the glossary and the language registry.

If `references/` or `scripts/` are missing (for example the skill was saved as a single file), download them from https://github.com/bitvault-developers/bvt-skills/tree/main/plugins/bvt-multi-language/skills/bvt-multi-language before continuing.

## The idea in simple words

There are two layers:

1. **Saved strings (always).** Every visible text lives in a language file (`en.json`, `hi.json`, ...), never inside the code. The app shows the file for the chosen language. Fast, offline, searchable by Google, cheap.
2. **Live translation (only when needed).** Text that changes all the time (chat, reviews, comments) or languages you did not prepare are translated on the fly through a translation service, with a cache.

Default = **hybrid**: layer 1 for all UI and public pages, layer 2 for user content plus an optional "Translate this page (beta)" fallback.

No translation service covers 500 languages. The biggest cover a few hundred, and quality drops for rare languages, so every language gets an honest **quality tier** (see Translating below).

Never use the old free Google Website Translator embed (`translate_a/element.js`, `google.translate.TranslateElement`). Google ended support for it. Replace it if you find it.

## Workflow checklist

Copy this list into your task list and tick it off:

1. Detect the platform (table below) and open its recipe in `references/platform-recipes.md`.
2. Pick languages. If the user names none, ship the base language plus the languages they mention; if they ask for "all" or "maximum", follow the coverage strategy below. Build the registry with `node scripts/make_registry.mjs`.
3. Externalize every visible string into key files (rules below). On an existing project, start with `python scripts/find_hardcoded.py <src>`.
4. Wire the platform library from the recipe.
5. Add the language switcher (rules below, component in the recipes file).
6. Make layout work for RTL and non-Latin scripts; format numbers and dates with Intl.
7. Public websites: per-language URLs, hreflang and sitemaps (`scripts/seo_hreflang.py`).
8. Fill translations (Translating below, details in `references/translating.md`).
9. Run the release gate (Quality gate below, details in `references/quality-checks.md`).

## Decision rules

1. **Saved strings first.** No hard-coded UI text, ever. Even a one-language MVP gets locale files and a switcher-ready structure.
2. **Library by platform:** Next.js → next-intl. Other React and React Native → i18next. Vue/Nuxt → vue-i18n / @nuxtjs/i18n. Svelte → Paraglide JS. Angular → Transloco (live switching). Flutter → gen-l10n + ARB. FlutterFlow → built-in Languages. Android → string resources + per-app language. iOS → String Catalogs. Electron/Tauri → i18next. WordPress → see recipe.
3. **Fallback chain for every lookup:** regional → base language → closest related language → default. Example: `pt-PT → pt → en`, `gsw → de → en`. Never show blank text or raw keys.
4. **Public pages are server-rendered per language** with their own URL (`/fr/...`). Client-only translation is invisible to Google and AI search.
5. **Live translation only for user content or unshipped languages**, always through your backend with a cache or on-device APIs. Never put a translation API key in client code.
6. **Detect, suggest, never force.** No automatic redirects based on IP.
7. **Currency follows the user's account or region, never the UI language.**
8. **Ask before spending:** print the translation cost estimate and get a yes before any paid run beyond the free tier.

## Platform detection

| Look for | Platform | Recipe section |
|---|---|---|
| `next.config.*` + `app/` | Next.js | Next.js App Router |
| `package.json` with `react`, no Next | React SPA | React |
| `app.json` / `expo` or `react-native` in package.json | React Native / Expo | React Native / Expo |
| `nuxt.config.*` / `vue` | Vue / Nuxt | Vue, Svelte, Angular |
| `svelte.config.*` | SvelteKit | Vue, Svelte, Angular |
| `angular.json` | Angular | Vue, Svelte, Angular |
| `pubspec.yaml` | Flutter | Flutter |
| FlutterFlow project / user says FlutterFlow | FlutterFlow | FlutterFlow |
| `build.gradle(.kts)` + `AndroidManifest.xml` | Android native | Android native |
| `*.xcodeproj` / `Package.swift` | iOS native | iOS native |
| `electron` / `src-tauri/` | Desktop | Desktop |
| `wp-config.php`, `wp-content/` | WordPress | WordPress |
| plain `.html` files | Static site | Plain HTML/JS |

## Key file rules

- **Keys** describe place and purpose: `checkout.payButton.label`, `errors.network.offline`. Not the English sentence (except gettext/PO projects).
- **Whole sentences only.** Never glue fragments (`"You have " + n + " coins"`). Use placeholders: `"You have {count} coins"`.
- **Plurals:** use the library's plural system (ICU `{count, plural, one {# coin} other {# coins}}` or i18next `_one`/`_other` keys). Languages need different forms: Arabic has 6, Chinese 1. `new Intl.PluralRules('ar').resolvedOptions().pluralCategories` lists them.
- **Context for translators:** add a description per key where the meaning is unclear (ARB `@key.description`, a `_context` comment file, or TMS notes). "Save" (button) and "Save" (discount) are different words in many languages.
- **Language tags:** BCP 47 (`pt-BR`, `zh-Hans`, `zh-Hant`, `sr-Latn`, `es-419`). Flutter/Android file names use `_` or `b+` forms; map them, don't invent tags.
- **Lazy-load:** ship only the active language file. 200 languages must not bloat the bundle.
- **Do not translate:** brand names, code, URLs, placeholders. Keep a glossary (see `references/translating.md`).
- **Translations are untrusted text.** Machine output, translators and TMS imports can contain HTML or script. Render strings as text (`textContent`, React children, Flutter `Text`); never put a translation into `innerHTML`, `dangerouslySetInnerHTML` or `v-html` unless it passes an allow-list sanitizer (for example DOMPurify with only `b`, `i`, `a`). Prefer rich-text APIs (`<Trans>` in react-i18next, `t.rich` in next-intl) that map tags to components.
- **Missing keys are bugs you can see.** In development, warn on every missing key; in production, log missing keys (key + language) to your error tracker instead of showing them.
- **Cache-bust language files.** Put a content hash in the file name or URL (`hi.3f9a1c.json`) so users get new translations after a release.

## Language registry

Keep one `languages.json` that every part of the app reads (switcher, SEO, fonts, tiers):

```json
[{ "code": "ar", "english": "Arabic", "native": "العربية", "script": "Arab", "dir": "rtl", "tier": "B", "fallback": "en" }]
```

Generate it with `node scripts/make_registry.mjs en,hi,ar,fr --tiers en=A,fr=B --fallback mr=hi --out languages.json`. It uses Intl plus the endonym table below and flags names a human should check. Store the native names in the registry. Don't rely on `Intl.DisplayNames` for native names at runtime: Chrome ships trimmed locale data, and in testing (Nov 2026) it returned the English name or the bare code for about 40 languages, including Odia, Assamese, Nepali, Sinhala, Burmese, Khmer, Lao, Georgian, Armenian, Basque, Welsh, Irish and Maltese. Node has fuller data, so generate there and keep the result:

```js
const RTL_SCRIPTS = new Set(['Arab', 'Hebr', 'Thaa', 'Syrc', 'Nkoo', 'Adlm', 'Rohg']);
const info = (code) => {
  const script = new Intl.Locale(code).maximize().script;
  return {
    code,
    english: new Intl.DisplayNames(['en'], { type: 'language' }).of(code),
    native: new Intl.DisplayNames([code], { type: 'language' }).of(code),
    script,
    dir: RTL_SCRIPTS.has(script) ? 'rtl' : 'ltr',
  };
};
```

Native names Chrome was missing, ready to paste into the registry:

```js
const ENDONYMS = { or: 'ଓଡ଼ିଆ', as: 'অসমীয়া', ne: 'नेपाली', si: 'සිංහල', sa: 'संस्कृतम्', bho: 'भोजपुरी', mai: 'मैथिली',
  ks: 'کٲشُر', ps: 'پښتو', ckb: 'کوردیی ناوەندی', ku: 'Kurdî', ug: 'ئۇيغۇرچە', yi: 'ייִדיש', dv: 'ދިވެހި',
  my: 'မြန်မာ', km: 'ខ្មែរ', lo: 'ລາວ', bo: 'བོད་སྐད་', ka: 'ქართული', hy: 'հայերեն', mn: 'монгол',
  ha: 'Hausa', yo: 'Èdè Yorùbá', ig: 'Asụsụ Igbo', zu: 'isiZulu', xh: 'isiXhosa', so: 'Soomaali',
  be: 'беларуская', is: 'íslenska', eu: 'euskara', gl: 'galego', ast: 'asturianu', oc: 'occitan',
  cy: 'Cymraeg', ga: 'Gaeilge', mt: 'Malti', lb: 'Lëtzebuergesch', gsw: 'Schwiizertüütsch', sq: 'shqip',
  fil: 'Filipino', qu: 'Runasimi', haw: 'ʻŌlelo Hawaiʻi', ht: 'Kreyòl ayisyen', mi: 'Te reo Māori' };
```

The language names inside sentences ("Marathi isn't translated yet") also come from `Intl.DisplayNames` in the UI language. Write those message templates so any name fits (for example Korean `{fallback}(으)로`, Indonesian `bahasa {fallback}`, Arabic `باللغة {fallback}`).

## Language switcher rules

- **Native names (endonyms):** "Deutsch", "العربية", "日本語", with the English name small next to them for search.
- **No flags.** Flags are countries, not languages.
- **Search box when there are more than 10 languages**, matching native name, English name and code, ignoring accents and case ("espanol" finds "español": compare `s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase()`). Put "Suggested" (detected) languages on top; sort the rest with `Intl.Collator`, not plain `<`.
- **Placement:** header top-right (top-left in RTL), again in the footer, and in Settings in apps. Show a globe/language icon **plus** the current language name.
- **On change:** update `<html lang>` and `dir` (or the platform equivalent), save the choice (localStorage/cookie + user profile when logged in), keep the user on the same page.
- **Order of signals:** the URL decides what a page shows; the saved choice decides where `/` sends a visitor; then device languages; then the default. IP location is a weak hint only.
- **Quality badge:** show "beta" next to machine-only (Tier D) languages.
- **Accessibility:** each option has its own `lang` attribute; keyboard reachable; the switcher's own labels come from translation keys too.

A ready React component (adapt it for other frameworks) is in `references/platform-recipes.md`, section Language switcher component.

## RTL, scripts, fonts, formatting

- **RTL** (Arabic, Hebrew, Persian, Urdu, Pashto, Sindhi, Uyghur, Yiddish, Dhivehi, Kurdish Sorani): set `dir="rtl"`; use CSS logical properties (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `text-align: start`); mirror directional icons (arrows, back), not logos, media controls or checkmarks; wrap user names and numbers in `<bdi>` or `unicode-bidi: isolate`.
- **Complex scripts** (Devanagari, Bengali, Tamil, Thai, Khmer, Myanmar, Ethiopic): rely on the platform text engine; never split strings by character. Thai, Khmer and Lao have no spaces, so use `Intl.Segmenter`/ICU for line breaks. CJK needs taller line height.
- **Fonts:** Noto families as fallback stack; load per script with `unicode-range` so Latin users don't download CJK fonts.
- **Text grows 30–40%** (more for short labels): no fixed-width buttons, allow wrapping, test with the pseudo-locale.
- **Formatting:** never hand-format. Use `Intl.NumberFormat`, `DateTimeFormat`, `RelativeTimeFormat`, `PluralRules`, `ListFormat`, `DisplayNames` (or Flutter `intl`, Android/iOS formatters). Currency comes from the user's account/region, not the UI language. Support other calendars if the market needs them.
- **Normalize** text to NFC before comparing, hashing or caching.
- **Sorting and search:** sort lists with `new Intl.Collator(lang).compare` (Swedish "ä" sorts after "z", Spanish "ñ" after "n"); search case- and accent-insensitively.
- **Time zones:** store times in UTC; show them with `Intl.DateTimeFormat(lang, { timeZone: userTimeZone })`. Language is not location.
- **Units:** metric or imperial follows the user's region or setting; format with `Intl.NumberFormat(lang, { style: 'unit', unit: 'kilometer' })`.
- **Forms:** names (one field "Full name" works worldwide; first/last order differs), addresses (country-specific fields and order), phone numbers (store E.164, format with libphonenumber), postal codes (not numeric everywhere). Never require Latin letters in name fields.

## SEO for public websites

- One URL per language, preferably subdirectories: `example.com/fr/`. Query params work but are weaker; cookie-only switching is invisible to crawlers.
- Every page lists all its language versions plus `x-default` with `<link rel="alternate" hreflang="..." href="...">`, and every version links back (reciprocal).
- Translate slugs, titles, meta descriptions and Open Graph tags; put all language URLs in the sitemap (`xhtml:link` alternates).
- Server-render translated HTML; client-only translations are mostly not indexed by search engines or AI crawlers.
- Machine translation is allowed when useful, but mass-producing low-value unreviewed pages risks Google's scaled-content policy. Review the top languages.
- Showing raw Google Translate output on indexable pages requires machine-translation markup and "powered by Google Translate" attribution.

## Translating

Translate **once, at build time**, and save the result in the language files. Only new or changed text is translated next time, and results are cached, so later runs cost almost nothing. Human-reviewed strings are locked and never overwritten.

### Quality tiers

| Tier | Meaning | How it's made | Switcher label |
|---|---|---|---|
| A, Reviewed | Human checked | MT or Claude draft + native reviewer | none |
| B, Premium MT | Strong engine + polish | DeepL/Google/Azure + Claude post-edit + glossary | none |
| C, Broad MT | Raw machine output | Google/Azure/Baidu for any language in their live list | none |
| D, Experimental | Rare languages, quality unknown | MADLAD-400 self-hosted or Claude | "beta" |
| E, Community | Not translated yet | Volunteers via Weblate/Tolgee/Crowdin | falls back, "help translate" |

Store the tier per language in `languages.json` (see Language registry above).

Default engine picks (full table with prices in `references/translating.md`; always read live language lists, counts change):
- **$0 budget:** Azure free (2M chars/month) or Google free (500K chars/month), cached; Claude for ICU messages and polish.
- **Best quality for main markets:** DeepL (European) or Google, then Claude post-edit with the glossary, then human review → Tier A.
- **Maximum coverage:** Google for breadth (around 190 API languages) → MADLAD-400 self-hosted or Claude for the rest as Tier D → Tier E community.
- **Private data (user content, KYC, messages):** on-device or self-hosted first; cloud only under a data processing agreement.
- **Never** use Meta NLLB-200 in commercial products (non-commercial licence).

### Maximum coverage strategy

When the user asks for "all languages" or "500+":

1. Run `--list-languages` for the main engine; that list is the Tier C ceiling.
2. Translate all of them (diff-only, cached). Print the cost estimate first.
3. Upgrade the top 5–20 markets to Tier B/A (post-edit + review).
4. Only if the user wants more: add Tier D languages via self-hosted MADLAD-400 or Claude, labeled "beta".
5. List remaining languages as Tier E with a "help translate" link to the TMS; they fall back to the closest language (e.g. `gsw → de`, `ast → es`, `oc → fr`).
6. A language also needs CLDR data (plurals, dates) and a font that covers its script. Check `new Intl.PluralRules(code)` and Noto coverage before promising it.

Tell the user plainly which tier each language landed in.

### Running the batch script

Copy `scripts/mt_translate.py` from this skill's folder into the project (for example `scripts/`). Python 3.8+, standard library only. API keys come from environment variables, never from code.

```bash
python scripts/mt_translate.py --list-languages --engine azure
python scripts/mt_translate.py --base src/locales/en.json --langs fr,hi,ar,zh-Hans --engine azure --glossary glossary.csv
python scripts/mt_translate.py ... --yes      # only after the user accepts the printed estimate
python scripts/mt_translate.py --base lib/l10n/app_en.arb --langs pt-BR,ar,zh-Hans=zh-CN --engine google --yes
```

Android, iOS, WordPress/PHP and other formats: convert first, translate, convert back, for example `python scripts/convert_locale_format.py app/src/main/res/values/strings.xml locales/en.json`, translate `locales/`, then `python scripts/convert_locale_format.py locales/hi.json app/src/main/res/values-hi/strings.xml`. Details in `references/translating.md`.

It translates only new or changed strings, protects placeholders and glossary terms, never overwrites reviewed strings, keeps extra plural forms, and writes status files to `<dir>/_meta/`. Engines: `google`, `azure`, `deepl`, `libre` (any LibreTranslate-compatible server), `anthropic` (Claude via the API, `ANTHROPIC_API_KEY`) and `mock` (tests). Classic engines skip ICU plural/select messages (translate those yourself); `anthropic` translates them, and with `--registry languages.json` also writes the plural forms each language needs that the base file lacks (Russian `_few`/`_many`, Arabic `_zero`/`_two`/`_few`/`_many`).

**Translating with Claude directly** (no API key): fine for small apps, ICU messages and post-editing. Keep placeholders, tags and ICU syntax byte-for-byte, produce every plural category the target language needs (`new Intl.PluralRules('ar').resolvedOptions().pluralCategories`), follow the glossary, and label the result as an AI draft until a native speaker reviews it.

## Quality gate

Copy `scripts/check_locales.py` into the project and run before every release:

```bash
python scripts/check_locales.py validate --base src/locales/en.json --registry languages.json --glossary glossary.csv   # 0 errors required
python scripts/check_locales.py pseudo --base src/locales/en.json --out src/locales/en-XA.json
python scripts/find_hardcoded.py src --ignore BrandName --strict
python scripts/screenshot_langs.py --url "http://localhost:3000/{lang}/" --langs en,ar,hi,de,ja,en-XA --base src/locales/en.json
python scripts/seo_hreflang.py check --dir dist --base https://example.com          # public websites
```

Then: look at the screenshots (an RTL language, a long-text language, a complex script and the pseudo-locale), review Tier B languages with Claude, get native sign-off for Tier A, check hreflang on public sites, and pass the legal checklist. Full steps, grep patterns, review prompt and legal checklist: `references/quality-checks.md`.

## Done when

- No hard-coded user-facing strings remain.
- Switcher works, is saved, updates `lang`/`dir`, and follows the rules above.
- Every language falls back cleanly; nothing blank or showing raw keys.
- RTL and pseudo-locale screenshots look right.
- Public sites: hreflang, x-default, sitemap and translated slugs in place.
- Each language shows its honest tier ("beta" for machine-only rare languages).
- `check_locales.py validate` passes with 0 errors, and `screenshot_langs.py` reports no problems.
- Translations render as text (no unsanitized HTML from translation files).