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
  libre     LIBRE_URL (default http://localhost:5000) (+ LIBRE_KEY); any LibreTranslate-compatible server
  anthropic ANTHROPIC_API_KEY (+ ANTHROPIC_MODEL, default claude-sonnet-5-5); Claude through the API.
            Also translates ICU plural/select messages, and with --registry writes the plural
            forms a language needs that the base file lacks (Russian _few/_many, Arabic _zero/_two/...).
  mock      no key; returns "[lang] text" for pipeline tests
In --langs, "app=engine" maps the app's tag to the engine's code (zh-Hans=zh-CN).
"""
import argparse, csv, hashlib, html, json, os, re, sys, time, unicodedata
import urllib.error, urllib.parse, urllib.request
from pathlib import Path

# list prices per 1M characters; "anthropic" is a rough token-based estimate - check current pricing
PRICE_PER_M = {"google": 20.0, "azure": 10.0, "deepl": 25.0, "libre": 0.0, "anthropic": 6.0, "mock": 0.0}
MAX_ITEMS = {"google": 100, "azure": 100, "deepl": 50, "libre": 1, "anthropic": 40, "mock": 100}
MAX_CHARS = 25000
PH = re.compile(r"(\{\{[^{}]+\}\}|\{[A-Za-z0-9_]+\}|%(?:\d+\$)?[sdif@]|<[^<>]+>)")
ICU = re.compile(r"\{\s*\w+\s*,\s*(?:plural|select|selectordinal)\s*,")
SPAN = re.compile(r'<span[^>]*?(?:translate="no"|notranslate)[^>]*>(.*?)</span>', re.S)
PLURAL = re.compile(r"^(.+)_(zero|one|two|few|many|other)$")  # i18next-style plural keys


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


CLAUDE_RULES = """You translate user-interface strings for a software product from {src} into {tgt}.
Rules:
- Return ONLY a JSON array of objects {{"id": ..., "text": ...}}, one per input item, same ids, nothing else.
- Keep every placeholder byte-for-byte: {{name}}, {{{{count}}}}, %s, %1$s, %d and HTML-like tags such as <b> or <a href="...">.
- ICU messages ({{count, plural, ...}} / select): keep the syntax and argument names, translate only the text
  inside the branches, and give the {tgt} plural categories ({cats}). Keep '#' where it is.
- An item with a "plural" field is one plural form: write the "{{plural}}" form of the message in {tgt}.
- Do not translate brand names, code, URLs or e-mail addresses. Glossary (term -> required translation): {glossary}
- Natural, concise UI wording for {tgt}. Keep the tone of the source. Do not add explanations."""


def claude_call(items, src, tgt, terms, cats):
    key = env("ANTHROPIC_API_KEY")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    gloss = json.dumps(terms, ensure_ascii=False) if terms else "none"
    system = CLAUDE_RULES.format(src=src, tgt=tgt, cats=", ".join(cats) if cats else "as the language needs",
                                 glossary=gloss)
    r = http_json("https://api.anthropic.com/v1/messages",
                  {"model": model, "max_tokens": 8000, "system": system,
                   "messages": [{"role": "user", "content": json.dumps(items, ensure_ascii=False)}]},
                  {"x-api-key": key, "anthropic-version": "2023-06-01"})
    text = "".join(b.get("text", "") for b in r.get("content", []) if b.get("type") == "text")
    m = re.search(r"\[.*\]", text, re.S)
    try:
        return {str(o["id"]): o["text"] for o in json.loads(m.group(0)) if isinstance(o.get("text"), str)}
    except Exception:
        return {}


def braces_ok(s):
    depth = 0
    for ch in s:
        depth += (ch == "{") - (ch == "}")
        if depth < 0:
            return False
    return depth == 0


def output_ok(source, out, plural=False):
    """Placeholders kept (a plural form may drop the number) and ICU braces balanced."""
    ps, po = sorted(PH.findall(source)), sorted(PH.findall(out))
    if not out.strip() or not braces_ok(out) or set(po) - set(ps):
        return False
    return plural or set(ps) <= set(po)


def tr_anthropic(items, src, tgt, terms, cats):
    """items: dicts {id, text[, plural]}; returns {id: translation} for outputs that pass output_ok."""
    done, todo = {}, list(items)
    for _ in range(2):  # one retry for items that came back missing or broken
        if not todo:
            break
        got = claude_call(todo, src, tgt, terms, cats)
        retry = []
        for it in todo:
            o = got.get(str(it["id"]))
            if o is not None and output_ok(it["text"], o, "plural" in it):
                done[str(it["id"])] = nfc(o)
            else:
                retry.append(it)
        todo = retry
    return done


ENGINES = {"google": tr_google, "azure": tr_azure, "deepl": tr_deepl, "libre": tr_libre,
           "anthropic": tr_anthropic, "mock": tr_mock}


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
    if engine == "anthropic":
        print("# Claude has no fixed list: big languages are strong, rare ones uneven (label them Tier D, 'beta').")
        return []
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


def load_registry(path):
    """languages.json from make_registry.mjs -> {code: [plural categories]}"""
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {e["code"]: e.get("plurals") or [] for e in data if isinstance(e, dict) and "code" in e}


def plural_groups(src):
    """i18next plural groups in the base file: {prefix: set(categories present)} (only groups with _other)."""
    groups = {}
    for k in src:
        m = PLURAL.match(k)
        if m:
            groups.setdefault(m.group(1), set()).add(m.group(2))
    return {g: c for g, c in groups.items() if "other" in c}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", help="base locale file, e.g. locales/en.json or lib/l10n/app_en.arb")
    ap.add_argument("--base-lang", default="en")
    ap.add_argument("--langs", help="comma list of target tags; app=engine to map codes")
    ap.add_argument("--engine", default="google", choices=sorted(ENGINES))
    ap.add_argument("--glossary", help="CSV with columns term,lang,translation (empty translation = keep as is)")
    ap.add_argument("--meta-dir", help="where status + cache files live (default: <base dir>/_meta)")
    ap.add_argument("--registry", help="languages.json (make_registry.mjs): plural categories per language")
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
    registry = load_registry(a.registry)
    groups = plural_groups(src)
    claude = a.engine == "anthropic"

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
        cats = registry.get(tag) or registry.get(tag.split("-")[0]) or []
        # plural forms this language needs that the base file lacks: (key, source text, category)
        extra = [(f"{g}_{c}", src[f"{g}_other"], c) for g, have in groups.items() for c in cats if c not in have]
        jobs = [(k, v, None) for k, v in src.items()] + extra
        for key, text, cat in jobs:
            h, m, cur = sha(nfc(text) + (f"|{cat}" if cat else "")), meta.get(key), tflat.get(key)
            if m and m.get("status") == "reviewed":
                if m.get("src") != h:
                    stale.append(key)
                continue
            if cur and m and m.get("src") == h:
                continue
            if cur and not m:  # existing translation nobody tracked: treat as human work
                meta[key] = {"src": h, "status": "reviewed", "engine": "existing"}
                continue
            if (ICU.search(text) or cat) and not claude:
                icu.append(key)
                continue
            ck = sha(f"{a.engine}|{eng_code}|{gver}|{cat or ''}|{nfc(text)}")
            prot = text if claude else protect(text, terms)
            todo.append((key, h, ck, prot, cat))
            if ck not in cache:
                total_chars += len(prot)
        plan.append(dict(tag=tag, eng=eng_code, tpath=tpath, tflat=tflat, meta=meta, mpath=mpath,
                         todo=todo, icu=icu, stale=stale, terms=terms, cats=cats))

    for p in plan:
        print(f"{p['tag']:>10}: {len(p['todo'])} to translate, {len(p['icu'])} ICU messages / plural forms "
              f"(use --engine anthropic or translate by hand), {len(p['stale'])} reviewed strings whose source changed")
        for label, keys in (("ICU/plural", p["icu"]), ("stale", p["stale"])):
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
        for _, _, ck, prot, cat in p["todo"]:
            if ck not in cache:
                uniq.setdefault(ck, (prot, cat))
        failed = []
        for chunk in batches([(ck, pc[0], pc[1]) for ck, pc in uniq.items()], a.engine):
            if claude:
                items = [{"id": ck, "text": t, **({"plural": cat} if cat else {})} for ck, t, cat in chunk]
                got = tr_anthropic(items, a.base_lang, p["eng"], p["terms"], p["cats"])
                for ck, _, _ in chunk:
                    if ck in got:
                        cache[ck] = got[ck]
                    else:
                        failed.append(ck)
            else:
                outs = ENGINES[a.engine]([t for _, t, _ in chunk], a.base_lang, p["eng"])
                for (ck, _, _), o in zip(chunk, outs):
                    cache[ck] = unprotect(o)
            cache_path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        for key, h, ck, _, _ in p["todo"]:
            if ck in cache:
                p["tflat"][key] = cache[ck]
                p["meta"][key] = {"src": h, "status": "machine", "engine": a.engine}
        if failed:
            print(f"{'':>12}{len(failed)} strings came back with broken placeholders or ICU and were left out; "
                  "translate them by hand")
        # keep keys still in the base file, plus extra plural forms of a base plural group (e.g. Arabic _few)
        keep = lambda k: k in src or (PLURAL.match(k) and PLURAL.match(k).group(1) in groups)
        for key in [k for k in p["tflat"] if not keep(k)]:
            p["tflat"].pop(key)
            p["meta"].pop(key, None)
        ordered = {k: p["tflat"][k] for k in src if k in p["tflat"]}
        ordered.update({k: v for k, v in p["tflat"].items() if k not in ordered})
        out = {"@@locale": p["tag"].replace("-", "_"), **ordered} if arb else (unflatten(ordered) if nested else ordered)
        p["tpath"].write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        p["mpath"].write_text(json.dumps(p["meta"], ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        print(f"wrote {p['tpath']}")


if __name__ == "__main__":
    main()
