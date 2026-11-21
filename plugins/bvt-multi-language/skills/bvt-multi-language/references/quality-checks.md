
# Checking translation quality

Run this before every release of a multilingual product, and whenever someone says a translation looks wrong. Setup is in `platform-recipes.md`; translating is in `translating.md`.

## Release gate

All must pass:

1. `check_locales.py validate` → 0 errors (missing, empty, placeholder, ICU braces).
2. Hard-coded string hunt → nothing user-facing left in code.
3. Pseudo-locale build looks right: every string bracketed and accented, nothing clipped.
4. RTL check (Arabic or Hebrew) and one complex-script check (Hindi, Thai or Chinese) on key screens.
5. Plural forms complete for each language (Arabic needs 6 categories, Polish/Russian 3–4). `check_locales.py validate --registry languages.json` reports missing i18next forms. List what each language needs with:
   `node -e 'for (const l of process.argv.slice(1)) console.log(l, new Intl.PluralRules(l).resolvedOptions().pluralCategories.join(","))' ar ru ja`
6. Claude review done for every Tier B language; native-speaker sign-off for Tier A.
7. Public sites: hreflang reciprocal, `x-default` present, codes valid, sitemap lists all languages.
8. Accessibility: `lang` and `dir` correct on every page/screen and each switcher option.
9. Legal/privacy checklist passed.

Report the result as a short table per language: errors, warnings, tier, reviewed yes/no.

## The QA script

Copy `scripts/check_locales.py` from this skill's folder into the project. Python 3.8+, standard library only.

```bash
python scripts/check_locales.py validate --base src/locales/en.json     # checks every sibling file
python scripts/check_locales.py validate --base src/locales/en.json --registry languages.json --glossary glossary.csv
python scripts/check_locales.py pseudo --base src/locales/en.json --out src/locales/en-XA.json
python scripts/check_locales.py validate --base lib/l10n/app_en.arb
```

Errors (exit code 1): missing key, empty value, a placeholder added or lost, broken ICU braces, and with `--registry` an i18next plural form the language needs but the file lacks (Russian `_few`/`_many`). Warnings: the same text as the source, text over 2.5× the source length, keys not in the base file, ICU plural messages missing a category the language uses, and with `--glossary` a glossary term whose required translation is missing.

The pseudo-locale (`en-XA`) wraps every string in `[ ... ~~~]`, adds accents and makes it about 35% longer, so hard-coded text and cut-off layouts stand out in screenshots.

## Hard-coded string hunt

Run the finder first, then move each hit into the locale files:

```bash
python scripts/find_hardcoded.py src --ignore BrandName,OtherBrand          # report
python scripts/find_hardcoded.py src lib --ignore BrandName --strict        # exit 1 in CI if anything is left
```

It covers React/JSX/TSX, Vue, Svelte, Angular, HTML, PHP, Flutter, Android layouts and Kotlin, and SwiftUI. It is a heuristic, so also search by hand where it can't see (emails, backend messages, images):

| Platform | Look for |
|---|---|
| React / Next / React Native | `rg -n '>[^<>{}]*[A-Za-z]{3,}[^<>{}]*<' --glob '*.{jsx,tsx}'`, plus `placeholder="`, `title="`, `aria-label="`, `alt="` with literal text |
| Vue / Svelte / Angular | literal text inside templates; attributes as above |
| Flutter | `rg -n "Text\(\s*['\"]" lib`, `hintText: '`, `labelText: '`, `tooltip: '` |
| Android | `rg -n 'android:text="[^@]' res`, `Text("` in Compose |
| iOS | `Text("` with sentences that are not keys; `NSLocalizedString` missing |
| Backend / email | subject lines, templates, error messages returned to users |

Also check: `toLocaleString()` without a locale, hand-built dates (`d + '/' + m`), string concatenation around variables, and images with text baked in.

## Screenshots in every language

```bash
python scripts/screenshot_langs.py --url "http://localhost:3000/{lang}/" --langs en,ar,hi,de,ja,en-XA --base src/locales/en.json
python scripts/screenshot_langs.py --url "http://localhost:5173/?lng={lang}" --langs en,ar --mobile
```

It saves one full-page screenshot per language and reports raw keys on screen (`home.title`), unfilled placeholders (`{name}`), a wrong `<html lang>`, a right-to-left language without `dir="rtl"`, JavaScript errors, and in the pseudo-locale any text that was not pseudo-translated (hard-coded). Needs Playwright (`pip install playwright && playwright install chromium`).

## hreflang and sitemaps (public websites)

```bash
python scripts/seo_hreflang.py generate --base https://example.com --langs en,fr,hi --default en --paths /,/pricing --sitemap dist/sitemap.xml
python scripts/seo_hreflang.py check --dir dist --base https://example.com
```

`check` reads the built HTML and fails on: no `lang` on `<html>`, a page that doesn't list itself, invalid codes, missing reciprocal links, and right-to-left pages without `dir="rtl"`. It warns on a missing `x-default` and on a canonical that points elsewhere.

## Claude review and post-editing

For each Tier B language (and as first pass for Tier A):

1. Take a sample: all strings under 4 words (buttons, menu items), all errors/warnings, and 50 random others.
2. Score each 1–5 on meaning, terminology (glossary), fluency, length fit, tone (formal/informal consistent).
3. Fix everything scoring 3 or less with minimal edits. Keep placeholders, tags and ICU syntax exactly.
4. Write fixes back to the locale file; keep `"status": "machine"` unless a human signs off.
5. Summarize: average score per language, top problem types, strings needing a native speaker.

Prompt pattern per chunk:

```text
You are reviewing UI translations from {source} to {target} for a {product type}.
Glossary (must follow): {glossary rows}. Tone: {formal|informal}. Context notes: {notes}.
For each key give: score 1-5, issue (if any), fixed text (only if score <= 3).
Never change placeholders like {name}, {{count}}, %1$s, HTML tags or ICU syntax.
Return JSON: {"key": {"score": n, "issue": "...", "fix": "..."}}
```

Be honest about rare languages: if Claude cannot judge quality reliably, say so and route the language to native-speaker review (Tier D stays "beta").

## Human review and translation management

Use a translation management system (TMS) once there are more than a handful of languages or any outside reviewers:

| Tool | Type | Free option |
|---|---|---|
| Weblate | Open source, Git-native | Self-host free; free hosting for open-source projects |
| Tolgee | Open source, in-context editing | Free self-host; small free cloud plan |
| Pontoon | Open source (Mozilla) | Self-host |
| Crowdin | SaaS, strong community features | Free plan for open-source projects |
| Lokalise, Phrase, Transifex, POEditor | SaaS | Trials / limited free plans |

Workflow: push base file → MT pre-fill → reviewers edit in context with screenshots → reviewed strings sync back and get `"status": "reviewed"` in `_meta/<lang>.json` so machine runs never overwrite them. Keep a translation memory so repeated strings are reused.

## Layout and script tests

Take screenshots of key screens (home, signup, checkout/wallet, settings, an error state) in:
- pseudo-locale (`en-XA`);
- one RTL language: layout mirrored, arrows flipped, logos and media controls not flipped, numbers and names isolated;
- one long-text language (German or Finnish): no clipped buttons, labels wrap;
- one complex script (Hindi, Thai or Khmer) and one CJK language: correct font, no boxes (tofu), line breaks sensible.

Check numbers, dates, currency and relative times are formatted per locale.

## Legal, privacy and accessibility checklist

- **Google Translate output shown raw:** "powered by Google Translate" attribution visible; indexable pages marked as machine-translated.
- **Personal data:** never sent to free MT tiers (DeepL free can use text for training); cloud MT covered by a data processing agreement and the privacy notice.
- **Licences:** no NLLB-200 in commercial products; AGPL LibreTranslate only as a separate service.
- **Quebec (Charter of the French Language):** commercial sites serving Quebec need a French version at least as available as the English one.
- **EU Accessibility Act (since June 2025)** for e-commerce sites and apps, via WCAG: 3.1.1 Language of Page and 3.1.2 Language of Parts → correct `lang` everywhere, including switcher options and mixed-language content.
- **Language tier honesty:** machine-only languages labeled "beta"; no claim of "500 languages" unless each is actually shipped and its tier is shown.