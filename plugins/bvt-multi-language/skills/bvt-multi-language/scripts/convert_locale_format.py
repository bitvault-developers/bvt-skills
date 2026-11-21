#!/usr/bin/env python3
"""Convert locale files between formats, so one translation pipeline serves every platform.

  python convert_locale_format.py app/src/main/res/values/strings.xml locales/en.json
  python convert_locale_format.py locales/hi.json app/src/main/res/values-hi/strings.xml
  python convert_locale_format.py languages/myplugin.pot locales/en.json          # WordPress
  python convert_locale_format.py locales/fr.json languages/myplugin-fr_FR.po
  python convert_locale_format.py Localizable.xcstrings locales/en.json --lang en  # iOS String Catalog
  python convert_locale_format.py locales/ja.json Localizable.xcstrings --lang ja  # adds/updates "ja" in place

Formats (by extension): .json (nested or flat i18next/next-intl style), .arb (Flutter), .po/.pot (gettext),
.xml (Android strings.xml), .xcstrings (iOS String Catalog).
Plurals map to i18next-style keys (key_one, key_few, key_other ...) in JSON, and back to
<plurals> (Android), plural variations (iOS) and msgid_plural (gettext; one/other only).
Standard library only. Python 3.8+.
"""
import argparse, json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

CATS = ("zero", "one", "two", "few", "many", "other")
PLURAL = re.compile(r"^(.+)_(zero|one|two|few|many|other)$")


# ---------- JSON / ARB ----------
def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        elif isinstance(v, str):
            out[key] = v
    return out


def unflatten(flat):
    root = {}
    for k, v in flat.items():
        cur = root
        *parents, last = k.split(".")
        for p in parents:
            nxt = cur.setdefault(p, {})
            if not isinstance(nxt, dict):  # "a" and "a.b" both exist: keep flat to avoid data loss
                return flat
            cur = nxt
        cur[last] = v
    return root


def read_json(path, lang):
    return flatten(json.loads(Path(path).read_text(encoding="utf-8")))


def write_json(path, strings, lang, nested=True):
    data = unflatten(strings) if nested else strings
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_arb(path, lang):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("@") and isinstance(v, str)}


COUNT = re.compile(r"%(?:\d+\$)?d|\{\{\s*count\s*\}\}|\{count\}")


def write_arb(path, strings, lang):
    """i18next plural groups (key_one/key_other...) become one ICU plural message, as Flutter expects."""
    out = {"@@locale": (lang or "en").replace("-", "_")}
    groups = {}
    for k in strings:
        m = PLURAL.match(k)
        if m and m.group(1) + "_other" in strings:
            groups.setdefault(m.group(1), []).append(m.group(2))
    for k, v in strings.items():
        m = PLURAL.match(k)
        if m and m.group(1) in groups:
            base = m.group(1)
            name = re.sub(r"[^A-Za-z0-9_]", "_", base)
            if name in out:
                continue
            forms = " ".join(f"{c}{{{COUNT.sub('{count}', strings[f'{base}_{c}'])}}}"
                             for c in sorted(groups[base], key=CATS.index))
            out[name] = "{count, plural, " + forms + "}"
            out["@" + name] = {"placeholders": {"count": {"type": "int"}}}
            continue
        out[re.sub(r"[^A-Za-z0-9_]", "_", k)] = v  # ARB keys must be valid Dart identifiers
    Path(path).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------- gettext PO / POT ----------
def po_unquote(s):
    return json.loads(s) if s.startswith('"') else s


def read_po(path, lang):
    """Key = msgctxt + '|' + msgid when a context exists, else msgid. Empty msgstr (POT) -> msgid."""
    out, cur, field = {}, {}, None

    def flush():
        if "msgid" in cur and cur["msgid"]:
            key = (cur.get("msgctxt", "") + "|" if cur.get("msgctxt") else "") + cur["msgid"]
            if "msgid_plural" in cur:
                out[key + "_one"] = cur.get("msgstr[0]") or cur["msgid"]
                out[key + "_other"] = cur.get("msgstr[1]") or cur["msgid_plural"]
            else:
                out[key] = cur.get("msgstr") or cur["msgid"]

    for line in Path(path).read_text(encoding="utf-8").splitlines() + [""]:
        line = line.strip()
        if not line:
            flush(); cur, field = {}, None
            continue
        if line.startswith("#"):
            continue
        m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(".*")$', line)
        if m:
            field = m.group(1)
            cur[field] = po_unquote(m.group(2))
        elif line.startswith('"') and field:
            cur[field] += po_unquote(line)
    return {k: v for k, v in out.items() if k}


def po_quote(s): return json.dumps(s, ensure_ascii=False)


def write_po(path, strings, lang):
    pot = Path(path).suffix == ".pot"
    lines = ['msgid ""', 'msgstr ""', po_quote("Content-Type: text/plain; charset=UTF-8\n")]
    if lang and not pot:
        lines.append(po_quote(f"Language: {lang.replace('-', '_')}\n"))
    lines.append("")
    done = set()
    for k, v in strings.items():
        m = PLURAL.match(k)
        if m and m.group(1) + "_other" in strings:
            base = m.group(1)
            if base in done:
                continue
            done.add(base)
            ctx, _, mid = base.rpartition("|")
            if ctx:
                lines.append("msgctxt " + po_quote(ctx))
            one, other = strings.get(base + "_one", strings[base + "_other"]), strings[base + "_other"]
            lines += ["msgid " + po_quote(mid), "msgid_plural " + po_quote(mid),
                      "msgstr[0] " + po_quote("" if pot else one), "msgstr[1] " + po_quote("" if pot else other), ""]
            continue
        ctx, _, mid = k.rpartition("|")
        if ctx:
            lines.append("msgctxt " + po_quote(ctx))
        lines += ["msgid " + po_quote(mid), "msgstr " + po_quote("" if pot else v), ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")


# ---------- Android strings.xml ----------
def android_unescape(s):
    s = (s or "").strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        s = s[1:-1]
    return re.sub(r"\\(['\"@?n])", lambda m: "\n" if m.group(1) == "n" else m.group(1), s)


def android_escape(s):
    s = s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
    return "\\" + s if s[:1] in ("@", "?") else s


def read_android(path, lang):
    out, root = {}, ET.parse(path).getroot()
    for el in root:
        if el.get("translatable") == "false":
            continue
        name = el.get("name")
        if el.tag == "string":
            out[name] = android_unescape("".join(el.itertext()))
        elif el.tag == "plurals":
            for item in el.findall("item"):
                out[f"{name}_{item.get('quantity')}"] = android_unescape("".join(item.itertext()))
        elif el.tag == "string-array":
            for i, item in enumerate(el.findall("item")):
                out[f"{name}.{i}"] = android_unescape("".join(item.itertext()))
    return out


def write_android(path, strings, lang):
    root = ET.Element("resources")
    groups, arrays, done = {}, {}, set()
    for k in strings:
        m = PLURAL.match(k)
        if m and m.group(1) + "_other" in strings:
            groups.setdefault(m.group(1), []).append(m.group(2))
        am = re.match(r"^(.+)\.(\d+)$", k)
        if am:
            arrays.setdefault(am.group(1), []).append(int(am.group(2)))
    for k, v in strings.items():
        m, am = PLURAL.match(k), re.match(r"^(.+)\.(\d+)$", k)
        if m and m.group(1) in groups:
            base = m.group(1)
            if base not in done:
                done.add(base)
                pl = ET.SubElement(root, "plurals", name=re.sub(r"[^A-Za-z0-9_]", "_", base))
                for c in sorted(groups[base], key=CATS.index):
                    ET.SubElement(pl, "item", quantity=c).text = android_escape(strings[f"{base}_{c}"])
        elif am and am.group(1) in arrays:
            base = am.group(1)
            if base not in done:
                done.add(base)
                arr = ET.SubElement(root, "string-array", name=re.sub(r"[^A-Za-z0-9_]", "_", base))
                for i in sorted(arrays[base]):
                    ET.SubElement(arr, "item").text = android_escape(strings[f"{base}.{i}"])
        else:
            ET.SubElement(root, "string", name=re.sub(r"[^A-Za-z0-9_]", "_", k)).text = android_escape(v)
    ET.indent(root) if hasattr(ET, "indent") else None
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text('<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n",
                          encoding="utf-8")


# ---------- iOS String Catalog (.xcstrings) ----------
def read_xcstrings(path, lang):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    lang = lang or data.get("sourceLanguage", "en")
    out = {}
    for key, entry in data.get("strings", {}).items():
        if entry.get("shouldTranslate") is False:
            continue
        loc = entry.get("localizations", {}).get(lang)
        if not loc:
            if lang == data.get("sourceLanguage", "en"):
                out[key] = key  # source strings may live only in the key
            continue
        if "stringUnit" in loc:
            out[key] = loc["stringUnit"].get("value", "")
        for cat, v in loc.get("variations", {}).get("plural", {}).items():
            out[f"{key}_{cat}"] = v.get("stringUnit", {}).get("value", "")
    return out


def write_xcstrings(path, strings, lang):
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"sourceLanguage": lang or "en", "strings": {},
                                                                         "version": "1.0"}
    lang = lang or data.get("sourceLanguage", "en")
    plural = {}
    for k in strings:
        m = PLURAL.match(k)
        if m and m.group(1) + "_other" in strings:
            plural.setdefault(m.group(1), []).append(m.group(2))
    for k, v in strings.items():
        m = PLURAL.match(k)
        if m and m.group(1) in plural:
            entry = data["strings"].setdefault(m.group(1), {})
            var = entry.setdefault("localizations", {}).setdefault(lang, {}).setdefault("variations", {})
            var.setdefault("plural", {})[m.group(2)] = {"stringUnit": {"state": "translated", "value": v}}
        else:
            entry = data["strings"].setdefault(k, {})
            entry.setdefault("localizations", {})[lang] = {"stringUnit": {"state": "translated", "value": v}}
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


READ = {".json": read_json, ".arb": read_arb, ".po": read_po, ".pot": read_po, ".xml": read_android,
        ".xcstrings": read_xcstrings}
WRITE = {".json": write_json, ".arb": write_arb, ".po": write_po, ".pot": write_po, ".xml": write_android,
         ".xcstrings": write_xcstrings}


def guess_lang(path):
    p = Path(path)
    m = re.search(r"values-(?:b\+)?([a-z]{2,3}(?:[-+_r]{1,2}[A-Za-z0-9]+)*)$", p.parent.name)  # values-pt-rBR
    if m:
        return re.sub(r"-r([A-Z]{2})", r"-\1", m.group(1)).replace("+", "-")
    for pat in (r"[_\-.]([a-z]{2,3}[_-](?:[A-Z]{2}|[A-Z][a-z]{3}))$", r"[_\-.]([a-z]{2,3})$",
                r"^([a-z]{2,3}(?:[_-](?:[A-Z]{2}|[A-Z][a-z]{3}|\d{3}))?)$"):
        m = re.search(pat, p.stem)
        if m:
            return m.group(1).replace("_", "-")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--lang", help="language tag of the strings (needed for .xcstrings; guessed from names otherwise)")
    ap.add_argument("--flat", action="store_true", help="write flat JSON keys instead of nested objects")
    a = ap.parse_args()
    s, d = Path(a.src), Path(a.dst)
    if s.suffix not in READ or d.suffix not in WRITE:
        sys.exit(f"Supported: {', '.join(sorted(READ))}")
    strings = READ[s.suffix](s, a.lang or guess_lang(s))
    lang = a.lang or guess_lang(d) or guess_lang(s)
    if d.suffix == ".json":
        # nest only dotted identifiers ("home.title"); sentence keys from gettext or iOS stay flat
        ident = all(re.fullmatch(r"[\w-]+(\.[\w-]+)*", k) for k in strings)
        write_json(d, strings, lang, nested=ident and not a.flat)
    else:
        WRITE[d.suffix](d, strings, lang)
    print(f"{s} -> {d}: {len(strings)} strings" + (f" ({lang})" if lang else ""))


if __name__ == "__main__":
    main()
