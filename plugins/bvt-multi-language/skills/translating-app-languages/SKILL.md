---
name: "translating-app-languages"
description: "Translates an app's locale files into many languages (Google, Azure, DeepL, LibreTranslate, MADLAD or Claude itself) with caching, glossaries, cost estimates and quality tiers, and adds live translation for user content. Use when adding languages, filling missing translations, or maximizing language coverage."
---

# Translating app languages

This skill fills locale files (JSON, ARB, and anything convertible to them) with translations, as cheaply and safely as possible, and adds live translation for content users write. It assumes the strings are already externalized (`adding-language-switching`). Quality checks before release live in `checking-translation-quality`.

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

Store the tier per language in `languages.json` (see `adding-language-switching`).

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
| Claude (this model) | Many, uneven | — | Tokens | Great for big languages, ICU messages, post-editing; weaker on rare languages |

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

Write this script into the project as `scripts/mt_translate.py` (Python 3.8+, standard library only). It:
- reads a base file (`en.json`, nested or flat, or Flutter `app_en.arb`);
- translates only new or changed strings, caching by hash of text + language + engine + glossary;
- protects placeholders (`{name}`, `{{count}}`, `%1$s`, HTML tags) and glossary terms by sending them as `translate="no"` spans;
- skips ICU plural/select messages (list printed) so Claude or a human translates them;
- never overwrites reviewed strings, and treats existing untracked translations as human work;
- removes keys deleted from the base file;
- writes status files in `<dir>/_meta/` and prints a cost estimate. Nothing is sent until `--yes`.

Usage:

```bash
python scripts/mt_translate.py --list-languages --engine azure
python scripts/mt_translate.py --base src/locales/en.json --langs fr,hi,ar,zh-Hans --engine azure --glossary glossary.csv
python scripts/mt_translate.py ... --yes      # after the user accepts the estimate
python scripts/mt_translate.py --base lib/l10n/app_en.arb --langs pt-BR,ar,zh-Hans=zh-CN --engine google --yes
```

`app=engine` maps the app's tag to the engine's code when they differ (Google uses `zh-CN`/`zh-TW`, DeepL uses `ZH-HANS`, `PT-BR`, `EN-US`). API keys come from env vars, never from code. Add `_meta/mt-cache.json` to version control only if the team wants shared caching; status files (`_meta/<lang>.json`) should be committed.

To mark strings as human-reviewed, set `"status": "reviewed"` in `_meta/<lang>.json` (a TMS sync script can do this).

```python
#!/usr/bin/env python3
"""Batch machine-translate a base locale file (JSON or Flutter ARB) into many languages.

Diff-only, cached, placeholder-safe, and it never overwrites reviewed strings.

  python mt_translate.py --base locales/en.json --langs fr,de,hi,ar,zh-Hans=zh-CN --engine google
  python mt_translate.py ... --yes                 # actually call the engine (may cost money)
  python mt_translate.py --list-languages --engine azure

Engines and env vars:
  google  GOOGLE_TRANSLATE_KEY
  azure   AZURE_TRANSLATOR_KEY (+ AZURE_TRANSLATOR_REGION for regional resources)
  deepl   DEEPL_KEY (keys ending in :fx use the free endpoint)
  libre   LIBRE_URL (default http://localhost:5000) (+ LIBRE_KEY)
  mock    no key; returns "[lang] text" for pipeline tests
In --langs, "app=engine" maps the app's tag to the engine's code (zh-Hans=zh-CN).
"""
import argparse, csv, hashlib, html, json, os, re, sys, time, unicodedata
import urllib.error, urllib.parse, urllib.request
from pathlib import Path

PRICE_PER_M = {"google": 20.0, "azure": 10.0, "deepl": 25.0, "libre": 0.0, "mock": 0.0}
MAX_ITEMS = {"google": 100, "azure": 100, "deepl": 50, "libre": 1, "mock": 100}
MAX_CHARS = 25000
PH = re.compile(r"(\{\{[^{}]+\}\}|\{[A-Za-z0-9_]+\}|%(?:\d+\$)?[sdif@]|<[^<>]+>)")
ICU = re.compile(r"\{\s*\w+\s*,\s*(?:plural|select|selectordinal)\s*,")
SPAN = re.compile(r'<span[^>]*?(?:translate="no"|notranslate)[^>]*>(.*?)</span>', re.S)


def nfc(s): return unicodedata.normalize("NFC", s)
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"Missing env var {name}")
    return v


def http_json(url, data=None, headers=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", **(headers or {})})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"HTTP {e.code} from {url.split('?')[0]}: {e.read()[:300]!r}")


# ---------- engines ----------
def tr_google(texts, src, tgt):
    url = "https://translation.googleapis.com/language/translate/v2?key=" + env("GOOGLE_TRANSLATE_KEY")
    r = http_json(url, {"q": texts, "source": src, "target": tgt, "format": "html"})
    return [t["translatedText"] for t in r["data"]["translations"]]


def tr_azure(texts, src, tgt):
    q = urllib.parse.urlencode({"api-version": "3.0", "from": src, "to": tgt, "textType": "html"})
    h = {"Ocp-Apim-Subscription-Key": env("AZURE_TRANSLATOR_KEY")}
    if os.environ.get("AZURE_TRANSLATOR_REGION"):
        h["Ocp-Apim-Subscription-Region"] = os.environ["AZURE_TRANSLATOR_REGION"]
    r = http_json("https://api.cognitive.microsofttranslator.com/translate?" + q, [{"Text": t} for t in texts], h)
    return [x["translations"][0]["text"] for x in r]


def deepl_host(key): return "api-free.deepl.com" if key.endswith(":fx") else "api.deepl.com"


def tr_deepl(texts, src, tgt):
    key = env("DEEPL_KEY")
    r = http_json(f"https://{deepl_host(key)}/v2/translate",
                  {"text": texts, "source_lang": src.split("-")[0].upper(), "target_lang": tgt.upper(),
                   "tag_handling": "html"}, {"Authorization": "DeepL-Auth-Key " + key})
    return [t["text"] for t in r["translations"]]


def libre_base(): return os.environ.get("LIBRE_URL", "http://localhost:5000").rstrip("/")


def tr_libre(texts, src, tgt):
    out = []
    for t in texts:
        d = {"q": t, "source": src.split("-")[0], "target": tgt, "format": "html"}
        if os.environ.get("LIBRE_KEY"):
            d["api_key"] = os.environ["LIBRE_KEY"]
        out.append(http_json(libre_base() + "/translate", d)["translatedText"])
    return out


def tr_mock(texts, src, tgt): return [f"[{tgt}] {t}" for t in texts]


ENGINES = {"google": tr_google, "azure": tr_azure, "deepl": tr_deepl, "libre": tr_libre, "mock": tr_mock}


def list_langs(engine):
    if engine == "google":
        r = http_json("https://translation.googleapis.com/language/translate/v2/languages?target=en&key="
                      + env("GOOGLE_TRANSLATE_KEY"))
        return [(l["language"], l.get("name", "")) for l in r["data"]["languages"]]
    if engine == "azure":
        r = http_json("https://api.cognitive.microsofttranslator.com/languages?api-version=3.0&scope=translation")
        return [(k, v.get("name", "")) for k, v in r["translation"].items()]
    if engine == "deepl":
        key = env("DEEPL_KEY")
        r = http_json(f"https://{deepl_host(key)}/v2/languages?type=target",
                      headers={"Authorization": "DeepL-Auth-Key " + key})
        return [(l["language"], l["name"]) for l in r]
    if engine == "libre":
        return [(l["code"], l["name"]) for l in http_json(libre_base() + "/languages")]
    return [("xx", "mock")]


# ---------- placeholder + glossary protection ----------
def wrap(s): return f'<span translate="no" class="notranslate">{html.escape(s, quote=False)}</span>'


def protect(text, terms):
    term_re = None
    if terms:
        alts = "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True))
        term_re = re.compile(rf"(?<!\w)(?:{alts})(?!\w)")
    out = []
    for i, part in enumerate(PH.split(text)):
        if i % 2:
            out.append(wrap(part))
            continue
        pos = 0
        if term_re:
            for m in term_re.finditer(part):
                out.append(html.escape(part[pos:m.start()], quote=False))
                out.append(wrap(terms[m.group(0)]))
                pos = m.end()
        out.append(html.escape(part[pos:], quote=False))
    return "".join(out)


def unprotect(text): return html.unescape(SPAN.sub(lambda m: m.group(1), text))


def load_glossary(path):
    if not path:
        return [], "none"
    raw = Path(path).read_text(encoding="utf-8")
    return [r for r in csv.DictReader(raw.splitlines()) if (r.get("term") or "").strip()], sha(raw)


def terms_for(rows, lang):
    m = {}
    for r in sorted(rows, key=lambda r: (r.get("lang") or "*") != "*"):  # '*' first, specific overrides
        if (r.get("lang") or "*") in ("*", lang):
            m[r["term"].strip()] = (r.get("translation") or "").strip() or r["term"].strip()
    return m


# ---------- file helpers ----------
def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out


def unflatten(flat):
    root = {}
    for k, v in flat.items():
        cur = root
        parts = k.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return root


def read_strings(data, arb):
    if arb:
        return {k: v for k, v in data.items() if not k.startswith("@")}
    return flatten(data)


def target_path(base, base_lang, tag):
    code = tag.replace("-", "_") if base.suffix == ".arb" else tag
    new_stem, n = re.subn(rf"(^|[_\-.]){re.escape(base_lang)}$", lambda m: m.group(1) + code, base.stem)
    if not n:
        sys.exit(f"Can't find '{base_lang}' at the end of {base.name}; name it like en.json or app_en.arb")
    return base.with_name(new_stem + base.suffix)


def batches(items, engine):
    cur, size = [], 0
    for it in items:
        if cur and (len(cur) >= MAX_ITEMS[engine] or size + len(it[1]) > MAX_CHARS):
            yield cur
            cur, size = [], 0
        cur.append(it)
        size += len(it[1])
    if cur:
        yield cur


def load_json(p): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", help="base locale file, e.g. locales/en.json or lib/l10n/app_en.arb")
    ap.add_argument("--base-lang", default="en")
    ap.add_argument("--langs", help="comma list of target tags; app=engine to map codes")
    ap.add_argument("--engine", default="google", choices=sorted(ENGINES))
    ap.add_argument("--glossary", help="CSV with columns term,lang,translation (empty translation = keep as is)")
    ap.add_argument("--meta-dir", help="where status + cache files live (default: <base dir>/_meta)")
    ap.add_argument("--yes", action="store_true", help="really call the engine")
    ap.add_argument("--list-languages", action="store_true")
    a = ap.parse_args()

    if a.list_languages:
        for code, name in list_langs(a.engine):
            print(f"{code}\t{name}")
        return
    if not a.base or not a.langs:
        ap.error("--base and --langs are required")

    base = Path(a.base)
    arb = base.suffix == ".arb"
    data = load_json(base)
    nested = not arb and any(isinstance(v, dict) for v in data.values())
    src = {k: v for k, v in read_strings(data, arb).items() if isinstance(v, str)}
    meta_dir = Path(a.meta_dir) if a.meta_dir else base.parent / "_meta"
    cache_path = meta_dir / "mt-cache.json"
    cache = load_json(cache_path)
    rows, gver = load_glossary(a.glossary)

    plan, total_chars = [], 0
    for item in filter(None, (x.strip() for x in a.langs.split(","))):
        tag, _, eng_code = item.partition("=")
        eng_code = eng_code or tag
        terms = terms_for(rows, tag)
        tpath = target_path(base, a.base_lang, tag)
        tflat = read_strings(load_json(tpath), arb)
        mpath = meta_dir / f"{tag}.json"
        meta = load_json(mpath)
        todo, icu, stale = [], [], []
        for key, text in src.items():
            h, m, cur = sha(nfc(text)), meta.get(key), tflat.get(key)
            if m and m.get("status") == "reviewed":
                if m.get("src") != h:
                    stale.append(key)
                continue
            if cur and m and m.get("src") == h:
                continue
            if cur and not m:  # existing translation nobody tracked: treat as human work
                meta[key] = {"src": h, "status": "reviewed", "engine": "existing"}
                continue
            if ICU.search(text):
                icu.append(key)
                continue
            ck = sha(f"{a.engine}|{eng_code}|{gver}|{nfc(text)}")
            prot = protect(text, terms)
            todo.append((key, h, ck, prot))
            if ck not in cache:
                total_chars += len(prot)
        plan.append(dict(tag=tag, eng=eng_code, tpath=tpath, tflat=tflat, meta=meta, mpath=mpath,
                         todo=todo, icu=icu, stale=stale))

    for p in plan:
        print(f"{p['tag']:>10}: {len(p['todo'])} to translate, {len(p['icu'])} ICU messages (translate with LLM/human), "
              f"{len(p['stale'])} reviewed strings whose source changed")
        for label, keys in (("ICU", p["icu"]), ("stale", p["stale"])):
            if keys:
                print(f"{'':>12}{label}: {', '.join(keys[:8])}{' ...' if len(keys) > 8 else ''}")
    cost = total_chars / 1e6 * PRICE_PER_M[a.engine]
    print(f"Uncached characters: {total_chars:,}  ~ ${cost:,.2f} at {a.engine} list price (free tier not subtracted)")
    if not a.yes and a.engine != "mock":
        print("Dry run only. Re-run with --yes to translate.")
        return

    meta_dir.mkdir(parents=True, exist_ok=True)
    for p in plan:
        uniq = {}
        for _, _, ck, prot in p["todo"]:
            if ck not in cache:
                uniq.setdefault(ck, prot)
        for chunk in batches(list(uniq.items()), a.engine):
            outs = ENGINES[a.engine]([t for _, t in chunk], a.base_lang, p["eng"])
            for (ck, _), o in zip(chunk, outs):
                cache[ck] = unprotect(o)
            cache_path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        for key, h, ck, _ in p["todo"]:
            p["tflat"][key] = cache[ck]
            p["meta"][key] = {"src": h, "status": "machine", "engine": a.engine}
        for key in [k for k in p["tflat"] if k not in src]:
            p["tflat"].pop(key)
            p["meta"].pop(key, None)
        ordered = {k: p["tflat"][k] for k in src if k in p["tflat"]}
        out = {"@@locale": p["tag"].replace("-", "_"), **ordered} if arb else (unflatten(ordered) if nested else ordered)
        p["tpath"].write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        p["mpath"].write_text(json.dumps(p["meta"], ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        print(f"wrote {p['tpath']}")


if __name__ == "__main__":
    main()
```

Glossary CSV (`term,lang,translation`; `*` = all languages; empty translation = keep the term as is):

```csv
term,lang,translation
YourBrand,*,
Wallet,hi,वॉलेट
```

## Translating with Claude directly

Use Claude itself (no API key) for: ICU plural/select messages the script skipped, small apps, post-editing machine output, and adding plural forms other languages need.

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