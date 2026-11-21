
# Translating

Fills locale files (JSON, ARB, and anything convertible to them) with translations, as cheaply and safely as possible, and adds live translation for content users write. It assumes the strings are already in language files (steps 1–5 of the workflow in `SKILL.md`). Quality checks before release are in `quality-checks.md`.

## The idea in simple words

- Translate **once, at build time**, and save the result in the language files. Only new or changed text gets translated next time, and results are cached, so the second run costs almost nothing.
- Every translated string remembers **who made it** (machine or human). Human-reviewed strings are locked and never overwritten.
- No service covers 500 languages. The biggest cover a few hundred (Google Translate is around 250, others far fewer), and quality drops a lot for rare languages. So every language gets an honest **quality tier**.

## Quality tiers

| Tier | Meaning | How it's made | Switcher label |
|---|---|---|---|
| A, Reviewed | Human checked | MT or Claude draft + native reviewer | none |
| B, Premium MT | Strong engine + polish | DeepL/Google/Azure + Claude post-edit + glossary | none |
| C, Broad MT | Raw machine output | Google/Azure/Baidu for any language in their live list | none |
| D, Experimental | Rare languages, quality unknown | MADLAD-400 self-hosted or Claude | "beta" |
| E, Community | Not translated yet | Volunteers via Weblate/Tolgee/Crowdin | falls back, "help translate" |

Store the tier per language in `languages.json` (built by `scripts/make_registry.mjs`, see Language registry in `SKILL.md`).

## Choosing the engine

Language counts and prices change often. Always read the live list with `--list-languages` and check the provider's pricing page before quoting numbers to the user. Approximate picture as of late 2026:

| Engine | Languages (approx.) | Free allowance | Paid (per 1M chars) | Notes |
|---|---|---|---|---|
| Google Cloud Translation | ~190 on API page (app shows ~250) | 500K chars/month | ~$20 | Broadest. Raw output shown to users needs "powered by Google Translate" attribution |
| Azure AI Translator | ~135 | 2M chars/month | ~$10 | Cheapest at volume |
| DeepL API | ~36 GA, expanding past 100 | Free tier (plans changing) | ~$25 + monthly fee | Best for European languages. Free tier text may be used for training: never send personal data |
| Amazon Translate | ~75 | 2M/month for 12 months | ~$15 | For AWS stacks |
| LibreTranslate / Argos (self-host) | ~45–50 | Free software (AGPL) | Your server | Data stays with you |
| MADLAD-400 (self-host) | 400+ on paper, only ~200 evaluated | Free (Apache 2.0, commercial OK) | Your GPU | Tier D only |
| Meta NLLB-200 | 200 | — | — | **Non-commercial licence: never use in commercial products** |
| Claude (`--engine anthropic`, or in chat) | Many, uneven | — | Tokens | Great for big languages, ICU messages, plural forms, post-editing; weaker on rare languages |

Default picks:
- **$0 budget:** Azure free (2M/month) or Google free (500K/month), cached; Claude for ICU messages and polish.
- **Best quality for main markets:** DeepL (European) or Google, then Claude post-edit with the glossary, then human review → Tier A.
- **Maximum coverage:** Google for breadth → MADLAD-400 or Claude for the rest as Tier D → Tier E community.
- **Private data (user content, KYC, messages):** on-device or self-hosted first; cloud only under a data processing agreement.

## Maximum coverage strategy

When the user asks for "all languages" or "500+":

1. Run `--list-languages` for the main engine; that list is the Tier C ceiling.
2. Translate all of them (diff-only, cached). Print the cost estimate first.
3. Upgrade the top 5–20 markets to Tier B/A (post-edit + review).
4. Only if the user wants more: add Tier D languages via self-hosted MADLAD-400 or Claude, labeled "beta".
5. List remaining languages as Tier E with a "help translate" link to the TMS; they fall back to the closest language (e.g. `gsw → de`, `ast → es`, `oc → fr`).
6. A language also needs CLDR data (plurals, dates) and a font that covers its script. Check `new Intl.PluralRules(code)` and Noto coverage before promising it.

Tell the user plainly which tier each language landed in.

## The batch script

The script lives in this skill's `scripts/` folder: copy `scripts/mt_translate.py` into the project (for example `scripts/`). Python 3.8+, standard library only.

Engines and environment variables (keys never go in code or in the repo):

| `--engine` | Key | Notes |
|---|---|---|
| `google` | `GOOGLE_TRANSLATE_KEY` | Broadest coverage |
| `azure` | `AZURE_TRANSLATOR_KEY` (+ `AZURE_TRANSLATOR_REGION`) | Cheapest at volume |
| `deepl` | `DEEPL_KEY` (keys ending `:fx` use the free endpoint) | Best for European languages |
| `libre` | `LIBRE_URL` (+ `LIBRE_KEY`) | Any LibreTranslate-compatible server, including a self-hosted one |
| `anthropic` | `ANTHROPIC_API_KEY` (+ `ANTHROPIC_MODEL`, default `claude-sonnet-5-5`) | Claude through the API. Also translates ICU plural/select messages |
| `mock` | none | Returns `[lang] text`, for testing the pipeline |

**Plural forms.** English has two plural categories (`one`, `other`); Russian needs four, Arabic six, Chinese one. With `--registry languages.json` the script knows each language's categories. The `anthropic` engine then writes the missing i18next keys (`coins_few`, `coins_many` for Russian; `_zero`, `_two`, `_few`, `_many` for Arabic) from the base `_other` string. Classic engines can't, so the script lists those keys for Claude or a person to write. Extra plural keys already in a target file are kept.

Every Claude answer is checked before it is saved: placeholders must match (a plural form may drop the number) and ICU braces must balance. Broken answers are retried once and otherwise left out and reported.

**Other file formats** (Android `strings.xml`, iOS `.xcstrings`, WordPress `.po`/`.pot`): convert to JSON, translate, convert back.

```bash
python scripts/convert_locale_format.py app/src/main/res/values/strings.xml locales/en.json
python scripts/mt_translate.py --base locales/en.json --langs hi,ar --engine azure --yes
python scripts/convert_locale_format.py locales/hi.json app/src/main/res/values-hi/strings.xml
python scripts/convert_locale_format.py languages/myplugin.pot locales/en.json        # WordPress
python scripts/convert_locale_format.py locales/fr.json languages/myplugin-fr_FR.po   # then compile .mo with msgfmt or Loco Translate
python scripts/convert_locale_format.py Localizable.xcstrings locales/en.json --lang en
python scripts/convert_locale_format.py locales/ja.json Localizable.xcstrings --lang ja  # updates the catalog in place
```

Plurals map to i18next-style `_one`/`_other` keys in JSON and back to Android `<plurals>`, iOS plural variations, Flutter ICU plurals (ARB) and gettext `msgid_plural` (one/other only).

Glossary CSV (`term,lang,translation`; `*` = all languages; empty translation = keep the term as is):

```csv
term,lang,translation
BitVault,*,
Wallet,hi,वॉलेट
```

## Translating with Claude directly

Use Claude itself (no API key) for: ICU plural/select messages the script skipped, small apps, post-editing machine output, and adding plural forms other languages need.

With an API key, `--engine anthropic` does this in batches. In chat, the same rules apply:

Rules:
- Work in chunks of about 100 keys per language; output **valid JSON with exactly the same keys**.
- Keep placeholders, HTML tags and ICU syntax byte-for-byte; translate only the human text inside ICU branches.
- **Plural forms:** produce every category the target language needs (`new Intl.PluralRules('ar').resolvedOptions().pluralCategories` → zero, one, two, few, many, other). For ICU add the missing branches; for i18next add `_zero`, `_two`, `_few`, `_many` keys.
- Follow the glossary and do-not-translate list; match the app's tone (formal/informal "you").
- Short UI labels: stay short; ask for screen context when a word is ambiguous.
- Record these strings as `"status": "machine", "engine": "claude"` in `_meta/<lang>.json`.
- For rare languages, say honestly that quality is unverified and mark the language Tier D.

**Post-editing machine output** (best known trick for low-resource languages: MT + LLM polish + glossary): give Claude the source, the MT result and the glossary; ask it to fix meaning errors, wrong terms, broken placeholders and unnatural phrasing, changing as little as possible.

## Live translation for user content

For chat, reviews, comments, listings, support tickets: translate on demand, never at build time.

Order of preference:
1. **On-device** (free, private): Chrome/Edge built-in Translator API on desktop browsers; Google ML Kit on Android/iOS/Flutter (`google_mlkit_translation`); Apple Translation framework on iOS 18+.
2. **Your backend + cache**: a small endpoint calls the MT API and stores results in a database/KV keyed by hash.
3. **Never** call the MT API from the client with an exposed key.

Browser on-device (progressive enhancement, check support first):

```js
async function translateOnDevice(text, sourceLanguage, targetLanguage) {
  if (!('Translator' in self)) return null;
  const avail = await Translator.availability({ sourceLanguage, targetLanguage });
  if (avail === 'unavailable') return null;
  const tr = await Translator.create({ sourceLanguage, targetLanguage }); // may download a model; call from a user click
  return tr.translate(text);
}
```

Backend endpoint pattern (TypeScript, fetch-style handler; swap the Map for Redis, KV, D1 or a DB table):

```ts
const cache = new Map<string, string>();
const sha = async (s: string) => Array.from(new Uint8Array(
  await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s))))
  .map(b => b.toString(16).padStart(2, '0')).join('');

export async function POST(req: Request) {
  // require a logged-in user + rate limit here
  const { texts, target } = await req.json();
  if (!Array.isArray(texts) || texts.length > 50 || !/^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$/.test(target))
    return new Response('bad request', { status: 400 });
  const keys = await Promise.all(texts.map((t: string) => sha(`${target}|${t.normalize('NFC')}`)));
  const out: string[] = keys.map(k => cache.get(k) ?? '');
  const miss = keys.map((k, i) => (cache.has(k) ? -1 : i)).filter(i => i >= 0);
  if (miss.length) {
    const r = await fetch(
      `https://translation.googleapis.com/language/translate/v2?key=${process.env.GOOGLE_TRANSLATE_KEY}`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: miss.map(i => texts[i]), target, format: 'text' }) });
    if (!r.ok) return new Response('translation failed', { status: 502 });
    const data = await r.json();
    miss.forEach((i, j) => { out[i] = data.data.translations[j].translatedText; cache.set(keys[i], out[i]); });
  }
  return Response.json({ translations: out, provider: 'Google Translate' });
}
```

UI rules for live translation: show a "Translated by …" label (required for raw Google output) and a "Show original" toggle; translate when the user taps, or automatically when their language differs and they enabled auto-translate; detect the source language (Chrome Language Detector API on-device, or the MT API's detect).

**"Translate this page (beta)" fallback** for languages not shipped: run page text through the same endpoint, mark the page with machine-translation notice, and do not let it replace server-rendered SEO pages.

## Cost and legal guardrails

- Always print the cost estimate and get a yes before any paid run beyond the free tier. Example: 10,000 strings × 80 chars × 100 languages = 80M chars ≈ $1,600 on Google or ≈ $800 on Azure for the **first** run; later runs only pay for changes.
- Google: visible "powered by Google Translate" attribution next to raw results; mark indexable raw output as machine-translated; don't use "Google" in product names. Long-term storage of raw Google output under current terms is unclear: human-edited strings saved as your own locale files are the safest position.
- DeepL free tier may use text for training: no personal or confidential data.
- NLLB-200 is non-commercial only. MADLAD-400 (Apache 2.0) and Opus-MT (CC-BY 4.0) allow commercial use; LibreTranslate is AGPL (fine as a separate service).
- User content to a cloud MT service = personal data processing: data processing agreement, privacy notice, EU region where possible.