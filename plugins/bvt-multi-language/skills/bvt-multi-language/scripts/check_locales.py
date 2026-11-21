#!/usr/bin/env python3
"""Locale QA: validate translations against the base file, or build a pseudo-locale.

  python check_locales.py validate --base locales/en.json        # checks every sibling locale file
  python check_locales.py validate --base locales/en.json --registry languages.json --glossary glossary.csv
  python check_locales.py pseudo --base locales/en.json --out locales/en-XA.json
Exit code 1 when any ERROR is found (missing key, empty value, broken placeholder, broken ICU braces,
and with --registry: a plural form the language needs but the file lacks).
--glossary adds a warning where a glossary term's required translation is missing from a string.
"""
import argparse, csv, json, math, re, sys
from pathlib import Path

PH = re.compile(r"\{\{[^{}]+\}\}|\{[A-Za-z0-9_]+\}|%(?:\d+\$)?[sdif@]|<[^<>]+>")
SPLIT = re.compile(r"(\{\{[^{}]+\}\}|%(?:\d+\$)?[sdif@]|<[^<>]+>|[{}])")
ACC = str.maketrans("aAcCeEgGiIlLnNoOsStTuUyYzZ", "áÅçÇéÉĝĜíÎļĻñÑóÖšŠţŢúÜýÝžŽ")


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        out.update(flatten(v, key)) if isinstance(v, dict) else out.__setitem__(key, v)
    return out


def unflatten(flat):
    root = {}
    for k, v in flat.items():
        cur = root
        *parents, last = k.split(".")
        for p in parents:
            cur = cur.setdefault(p, {})
        cur[last] = v
    return root


def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if Path(path).suffix == ".arb":
        return {k: v for k, v in data.items() if not k.startswith("@")}, data, False
    return flatten(data), data, any(isinstance(v, dict) for v in data.values())


def braces_ok(s):
    depth = 0
    for ch in s:
        depth += (ch == "{") - (ch == "}")
        if depth < 0:
            return False
    return depth == 0


PLURAL = re.compile(r"^(.+)_(zero|one|two|few|many|other)$")  # i18next-style plural keys
ICU_PLURAL = re.compile(r"\{\s*\w+\s*,\s*(?:plural|selectordinal)\s*,")
NOT_LOCALES = {"languages.json", "glossary.json", "package.json", "tsconfig.json"}


def icu_categories(s):
    """Plural categories used in the first ICU plural message of s (exact =N selectors ignored)."""
    m = ICU_PLURAL.search(s)
    if not m:
        return None
    depth, i, cats, word = 1, m.end(), set(), ""
    while i < len(s) and depth:
        ch = s[i]
        if ch == "{":
            if depth == 1 and word.strip() and not word.strip().startswith("="):
                cats.add(word.strip().split()[-1])
            depth += 1
            word = ""
        elif ch == "}":
            depth -= 1
            word = ""
        elif depth == 1:
            word += ch
        i += 1
    return cats


def lang_of(path, base_path, base_lang):
    """'app_pt_BR.arb' next to 'app_en.arb' -> 'pt-BR'; 'hi.json' next to 'en.json' -> 'hi'."""
    stem, bstem = Path(path).stem, Path(base_path).stem
    prefix = bstem[: len(bstem) - len(base_lang)] if bstem.endswith(base_lang) else ""
    code = stem[len(prefix):] if prefix and stem.startswith(prefix) else stem
    return code.replace("_", "-")


def load_registry(path):
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {e["code"]: e.get("plurals") or [] for e in data if isinstance(e, dict) and "code" in e}


def load_glossary(path):
    if not path:
        return []
    rows = csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines())
    return [r for r in rows if (r.get("term") or "").strip()]


def compare(key, s, t, plural, errs, warns):
    if not isinstance(t, str) or not t.strip():
        errs.append(f"empty    {key}")
        return
    ps, pt = set(PH.findall(s)), set(PH.findall(t))
    if pt - ps:
        errs.append(f"placeholder {key}: added {sorted(pt - ps)}")
    if ps - pt:
        # a plural form may leave the number out ("one coin", Arabic dual); anywhere else it is a bug
        (warns if plural else errs).append(f"placeholder {key}: lost {sorted(ps - pt)}")
    if not braces_ok(t):
        errs.append(f"ICU braces {key}")
    core = PH.sub("", s).strip()
    if t == s and len(core) >= 4 and re.search(r"[^\W\d_]", core):
        warns.append(f"same as source {key}")
    if len(s) >= 8 and len(t) > 2.5 * len(s):
        warns.append(f"long ({len(t)}/{len(s)} chars) {key}")


def validate(base_path, base_lang="en", registry_path=None, glossary_path=None):
    base_path = Path(base_path)
    src, _, _ = load(base_path)
    registry, glossary = load_registry(registry_path), load_glossary(glossary_path)
    siblings = sorted(p for p in base_path.parent.glob("*" + base_path.suffix)
                      if p != base_path and p.name not in NOT_LOCALES)
    groups = {}
    for k in src:
        m = PLURAL.match(k)
        if m:
            groups.setdefault(m.group(1), set()).add(m.group(2))
    groups = {g for g, c in groups.items() if "other" in c}
    errors = 0
    for f in siblings:
        tgt, _, _ = load(f)
        lang = lang_of(f, base_path, base_lang)
        cats = registry.get(lang) or registry.get(lang.split("-")[0]) or []
        errs, warns = [], []
        for key, s in src.items():
            if not isinstance(s, str):
                continue
            m = PLURAL.match(key)
            t = tgt.get(key)
            if t is None:
                if m and m.group(2) != "other" and isinstance(tgt.get(m.group(1) + "_other"), str):
                    continue  # this language may not use that plural category; runtime falls back to _other
                errs.append(f"missing  {key}")
                continue
            compare(key, s, t, bool(m), errs, warns)
        for key, t in tgt.items():
            if key in src:
                continue
            m = PLURAL.match(key)
            if m and isinstance(src.get(m.group(1) + "_other"), str):
                compare(key, src[m.group(1) + "_other"], t, True, errs, warns)  # extra category, e.g. Arabic _few
            else:
                warns.append(f"extra key {key}")
        if cats and not lang.endswith("XA"):
            for g in sorted(groups):  # i18next plural groups: every category this language uses must exist
                for c in cats:
                    if not isinstance(tgt.get(f"{g}_{c}"), str):
                        errs.append(f"plural   {g}_{c} ({lang} needs: {', '.join(cats)})")
            for key, t in tgt.items():  # ICU plural messages: categories should match the language
                have = icu_categories(t) if isinstance(t, str) else None
                if have is not None and set(cats) - have - {"other"} and "other" in have:
                    warns.append(f"ICU plural {key}: missing {sorted(set(cats) - have)} for {lang}")
        for r in glossary:
            if (r.get("lang") or "*") not in ("*", lang):
                continue
            term, want = r["term"].strip(), (r.get("translation") or "").strip() or r["term"].strip()
            for key, s in src.items():
                t = tgt.get(key)
                if isinstance(s, str) and isinstance(t, str) and re.search(rf"(?<!\w){re.escape(term)}(?!\w)", s) \
                        and want not in t:
                    warns.append(f"glossary {key}: expected '{want}' for '{term}'")
        print(f"\n{f.name}: {len(errs)} errors, {len(warns)} warnings")
        for line in errs[:50]:
            print("  ERROR", line)
        for line in warns[:30]:
            print("  warn ", line)
        errors += len(errs)
    print(f"\nChecked {len(siblings)} files against {base_path.name}: {errors} errors total")
    return 1 if errors else 0


def pseudo_text(text):
    out, depth = [], 0
    for tok in filter(None, SPLIT.split(text)):
        if tok in "{}" and len(tok) == 1:
            depth += 1 if tok == "{" else -1
            out.append(tok)
        elif PH.fullmatch(tok) or depth % 2 == 1:  # placeholders and ICU syntax stay untouched
            out.append(tok)
        else:
            out.append(tok.translate(ACC))
    return f"[{''.join(out)} {'~' * max(1, math.ceil(len(text) * 0.35))}]"


def pseudo(base_path, out_path):
    flat, raw, nested = load(base_path)
    res = {k: pseudo_text(v) if isinstance(v, str) else v for k, v in flat.items()}
    if Path(base_path).suffix == ".arb":
        res = {"@@locale": Path(out_path).stem.split("_", 1)[-1], **res}
    elif nested:
        res = unflatten(res)
    Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({len(flat)} strings)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("--base", required=True); v.add_argument("--base-lang", default="en")
    v.add_argument("--registry", help="languages.json with plural categories per language")
    v.add_argument("--glossary", help="CSV term,lang,translation")
    p = sub.add_parser("pseudo"); p.add_argument("--base", required=True); p.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.exit(validate(a.base, a.base_lang, a.registry, a.glossary) if a.cmd == "validate" else pseudo(a.base, a.out))
