---
name: "checking-translation-quality"
description: "Checks a multilingual product before release - missing keys, broken placeholders and ICU syntax, untranslated or overlong strings, hard-coded text, pseudo-locale and RTL layout tests, Claude review and post-editing, human review, and attribution, privacy and language-law checks. Use before shipping translations or when translation quality is questioned."
---

# Checking translation quality

Run this before every release of a multilingual product, and whenever someone says a translation looks wrong. Setup lives in `adding-language-switching`; translating lives in `translating-app-languages`.

## Release gate

All must pass:

1. `check_locales.py validate` → 0 errors (missing, empty, placeholder, ICU braces).
2. Hard-coded string hunt → nothing user-facing left in code.
3. Pseudo-locale build looks right: every string bracketed and accented, nothing clipped.
4. RTL check (Arabic or Hebrew) and one complex-script check (Hindi, Thai or Chinese) on key screens.
5. Plural forms complete for each language (Arabic needs 6 categories, Polish/Russian 3–4). List what each language needs with:
   `node -e 'for (const l of process.argv.slice(1)) console.log(l, new Intl.PluralRules(l).resolvedOptions().pluralCategories.join(","))' ar ru ja`
6. Claude review done for every Tier B language; native-speaker sign-off for Tier A.
7. Public sites: hreflang reciprocal, `x-default` present, codes valid, sitemap lists all languages.
8. Accessibility: `lang` and `dir` correct on every page/screen and each switcher option.
9. Legal/privacy checklist passed.

Report the result as a short table per language: errors, warnings, tier, reviewed yes/no.

## The QA script

Write this into the project as `scripts/check_locales.py` (Python 3.8+, standard library only).

```bash
python scripts/check_locales.py validate --base src/locales/en.json     # checks every sibling file
python scripts/check_locales.py pseudo --base src/locales/en.json --out src/locales/en-XA.json
python scripts/check_locales.py validate --base lib/l10n/app_en.arb
```

`validate` reports per file: ERROR for missing key, empty value, placeholder lost/added, broken ICU braces (exit code 1); warn for text identical to source, text over 2.5× longer than source, and extra keys. It understands i18next plural keys (`_zero`, `_one`, `_two`, `_few`, `_many`, `_other`): a language may skip categories it doesn't use as long as `_other` exists, may add categories the base lacks (Arabic `_few`), and a plural form that leaves out the number ("one coin", Arabic dual) is only a warning. `pseudo` writes an accented, ~35% longer, bracketed copy (`[Wáļļéţ ~~~]`) that keeps placeholders and ICU syntax intact. Register it as a dev-only language to spot hard-coded text (anything without brackets) and clipped layouts (missing `]`).

```python
#!/usr/bin/env python3
"""Locale QA: validate translations against the base file, or build a pseudo-locale.

  python check_locales.py validate --base locales/en.json        # checks every sibling locale file
  python check_locales.py pseudo --base locales/en.json --out locales/en-XA.json
Exit code 1 when any ERROR is found (missing key, empty value, broken placeholder, broken ICU braces).
"""
import argparse, json, math, re, sys
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


def validate(base_path):
    base_path = Path(base_path)
    src, _, _ = load(base_path)
    siblings = sorted(p for p in base_path.parent.glob("*" + base_path.suffix) if p != base_path)
    errors = 0
    for f in siblings:
        tgt, _, _ = load(f)
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
    v = sub.add_parser("validate"); v.add_argument("--base", required=True)
    p = sub.add_parser("pseudo"); p.add_argument("--base", required=True); p.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.exit(validate(a.base) if a.cmd == "validate" else pseudo(a.base, a.out))
```

## Hard-coded string hunt

Search for visible text that skipped the translation system, then move each hit into the locale files:

| Platform | Look for |
|---|---|
| React / Next / React Native | `rg -n '>[^<>{}]*[A-Za-z]{3,}[^<>{}]*<' --glob '*.{jsx,tsx}'`, plus `placeholder="`, `title="`, `aria-label="`, `alt="` with literal text |
| Vue / Svelte / Angular | literal text inside templates; attributes as above |
| Flutter | `rg -n "Text\(\s*['\"]" lib`, `hintText: '`, `labelText: '`, `tooltip: '` |
| Android | `rg -n 'android:text="[^@]' res`, `Text("` in Compose |
| iOS | `Text("` with sentences that are not keys; `NSLocalizedString` missing |
| Backend / email | subject lines, templates, error messages returned to users |

Also check: `toLocaleString()` without a locale, hand-built dates (`d + '/' + m`), string concatenation around variables, and images with text baked in.

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