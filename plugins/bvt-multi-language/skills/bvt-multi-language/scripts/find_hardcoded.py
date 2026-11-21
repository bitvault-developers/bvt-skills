#!/usr/bin/env python3
"""Find user-facing text that is still hard-coded instead of coming from a language file.

  python find_hardcoded.py src
  python find_hardcoded.py src lib --ignore BitVault,BVT --strict      # exit 1 if anything is found (CI)
  python find_hardcoded.py . --json > hardcoded.json

Covers React/JSX/TSX, Vue, Svelte, Angular templates, HTML, PHP (WordPress), Flutter/Dart, Android XML and
Kotlin/Compose, and SwiftUI. It is a heuristic: it flags likely text (letters, not code-looking tokens) in the
places users see it (element text, placeholder/title/alt/aria-label attributes, Text(...) widgets, echo).
Skips node_modules, build folders, tests, stories and locale files. Standard library only. Python 3.8+.
"""
import argparse, json, re, sys
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "out", "coverage", "vendor",
             "Pods", ".dart_tool", "locales", "l10n", "i18n", "lang", "languages", "translations", "__pycache__",
             "_meta", "generated", ".gradle", "DerivedData"}
SKIP_FILE = re.compile(r"(\.test\.|\.spec\.|\.stories\.|\.d\.ts$|\.min\.)")
ATTRS = r"(?:placeholder|title|alt|aria-label|aria-description|label|helperText|tooltip|content)"

RULES = {
    "jsx": [  # text between tags, and visible attributes with a plain string
        (re.compile(r">\s*([^<>{}\n]*[A-Za-z\u00C0-\uFFFF][^<>{}\n]*?)\s*<"), "element text"),
        (re.compile(ATTRS + r"""\s*=\s*["']([^"'{}]*[A-Za-z][^"'{}]*)["']"""), "attribute"),
    ],
    "vue": [
        (re.compile(r">\s*([^<>{}\n]*[A-Za-z\u00C0-\uFFFF][^<>{}\n]*?)\s*<"), "element text"),
        (re.compile(r"(?<![:@\-])\b" + ATTRS + r"""\s*=\s*["']([^"'{}]*[A-Za-z][^"'{}]*)["']"""), "attribute"),
    ],
    "php": [
        (re.compile(r"""\becho\s+["']([^"'<>]*[A-Za-z][^"'<>]*)["']"""), "echo"),
        (re.compile(r">\s*([^<>{}\n?]*[A-Za-z][^<>{}\n?]*?)\s*<"), "element text"),
    ],
    "dart": [
        (re.compile(r"""\bText\(\s*['"]([^'"$]*[A-Za-z][^'"$]*)['"]"""), "Text()"),
        (re.compile(r"""\b(?:labelText|hintText|helperText|tooltip|title|semanticsLabel)\s*:\s*['"]([^'"$]*[A-Za-z][^'"$]*)['"]"""),
         "named argument"),
    ],
    "kotlin": [
        (re.compile(r"""\bText\(\s*(?:text\s*=\s*)?"([^"$]*[A-Za-z][^"$]*)\""""), "Text()"),
        (re.compile(r"""\b(?:setText|Toast\.makeText\([^,]+,)\s*\(?\s*"([^"$]*[A-Za-z][^"$]*)\""""), "setText/Toast"),
    ],
    "xml": [
        (re.compile(r"""android:(?:text|hint|contentDescription|title)\s*=\s*"(?!@)([^"]*[A-Za-z][^"]*)\""""), "attribute"),
    ],
    "swift": [
        (re.compile(r"""\b(?:Text|Button|Label|navigationTitle|Toggle)\(\s*"([^"\\]*[A-Za-z][^"\\]*)\""""), "SwiftUI"),
    ],
}
EXT = {".jsx": "jsx", ".tsx": "jsx", ".js": "jsx", ".ts": "jsx", ".html": "vue", ".htm": "vue", ".vue": "vue",
       ".svelte": "vue", ".php": "php", ".dart": "dart", ".kt": "kotlin", ".java": "kotlin", ".xml": "xml",
       ".swift": "swift"}
CODEY = re.compile(r"^[\w.\-/:#@%$&*+=|\\]+$")  # identifiers, paths, URLs, CSS classes


def looks_like_text(s, ignore):
    s = s.strip()
    if len(s) < 2 or not re.search(r"[^\W\d_]{2,}", s):
        return False
    if s in ignore or all(w in ignore for w in re.findall(r"[^\W\d_]+", s)):
        return False
    if CODEY.match(s) and " " not in s and not re.match(r"^[A-Z][a-z]+$", s):
        return False  # one code-looking token; capitalised single words ("Save") are still reported
    if re.search(r"(=>|&&|\|\||\bfunction\b|\breturn\b|;\s*$|^\s*//|\bconst\b|\bimport\b)", s):
        return False
    return True


def scan_file(path, ignore):
    kind = EXT.get(path.suffix.lower())
    if not kind:
        return []
    if kind == "xml" and "/res/layout" not in path.as_posix() and "/res/menu" not in path.as_posix():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    if kind == "jsx" and path.suffix in (".js", ".ts") and "<" not in text:
        return []
    hits = []
    for rx, label in RULES[kind]:
        for m in rx.finditer(text):
            s = m.group(1).strip()
            if looks_like_text(s, ignore):
                line = text.count("\n", 0, m.start(1)) + 1
                hits.append({"file": str(path), "line": line, "kind": label, "text": s[:120]})
    return hits


def walk(roots):
    for root in roots:
        root = Path(root)
        if root.is_file():
            yield root
            continue
        for p in root.rglob("*"):
            if p.is_file() and not any(part in SKIP_DIRS for part in p.parts) and not SKIP_FILE.search(p.name):
                yield p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--ignore", default="", help="comma list of words to allow (brand names, units)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is found")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    ignore = {w.strip() for w in a.ignore.split(",") if w.strip()}
    hits = [h for p in walk(a.paths) for h in scan_file(p, ignore)]
    if a.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        for h in hits:
            print(f"{h['file']}:{h['line']}  [{h['kind']}]  {h['text']}")
        print(f"\n{len(hits)} likely hard-coded strings in {len({h['file'] for h in hits})} files")
    sys.exit(1 if a.strict and hits else 0)


if __name__ == "__main__":
    main()
