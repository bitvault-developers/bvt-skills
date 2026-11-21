#!/usr/bin/env python3
"""hreflang tags and a multilingual sitemap for a public website, and a checker for a built site.

  # print the <link> tags for every page and write sitemap.xml (one URL per language: /<lang>/<path>)
  python seo_hreflang.py generate --base https://example.com --langs en,fr,hi,ar --default en \\
      --paths /,/pricing,/blog/hello --sitemap dist/sitemap.xml
  # same, but the default language lives at the root (/pricing) instead of /en/pricing
  python seo_hreflang.py generate ... --default-at-root

  # check a built site: html lang, self link, x-default, reciprocal links, valid codes
  python seo_hreflang.py check --dir dist --base https://example.com

Exit code 1 from "check" when any ERROR is found. Standard library only. Python 3.8+.
"""
import argparse, re, sys
from html.parser import HTMLParser
from pathlib import Path
from xml.sax.saxutils import escape

TAG = re.compile(r"^(?:x-default|[a-z]{2,3}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|\d{3}))?)$")


def url_for(base, lang, path, default, at_root):
    path = "/" + path.strip("/") if path.strip("/") else "/"
    if at_root and lang == default:
        return base.rstrip("/") + path
    return base.rstrip("/") + f"/{lang}" + ("" if path == "/" else path) + ("/" if path == "/" else "")


def generate(a):
    langs = [l.strip() for l in a.langs.split(",") if l.strip()]
    default = a.default or langs[0]
    paths = [p.strip() for p in a.paths.split(",")] if a.paths else ["/"]
    entries = []
    for path in paths:
        alts = {l: url_for(a.base, l, path, default, a.default_at_root) for l in langs}
        alts["x-default"] = url_for(a.base, default, path, default, a.default_at_root)
        print(f"<!-- {path} : put in the <head> of every language version -->")
        for l, u in alts.items():
            print(f'<link rel="alternate" hreflang="{l}" href="{u}">')
        for l in langs:
            entries.append((alts[l], alts))
    if a.sitemap:
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
        for loc, alts in entries:
            out.append(f"  <url><loc>{escape(loc)}</loc>")
            for l, u in alts.items():
                out.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{escape(u)}"/>')
            out.append("  </url>")
        out.append("</urlset>")
        Path(a.sitemap).parent.mkdir(parents=True, exist_ok=True)
        Path(a.sitemap).write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"\nwrote {a.sitemap} ({len(entries)} URLs)")
    return 0


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang, self.dir, self.alts, self.canonical = None, None, {}, None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang, self.dir = d.get("lang"), d.get("dir")
        elif tag == "link" and (d.get("rel") or "").lower() == "alternate" and d.get("hreflang"):
            self.alts[d["hreflang"]] = d.get("href", "")
        elif tag == "link" and (d.get("rel") or "").lower() == "canonical":
            self.canonical = d.get("href")


def page_url(file, root, base):
    rel = file.relative_to(root).as_posix()
    rel = re.sub(r"(^|/)index\.html?$", r"\1", rel)
    rel = re.sub(r"\.html?$", "", rel)
    return base.rstrip("/") + "/" + rel


def norm(u): return u.rstrip("/") if u else u


def check(a):
    root, base = Path(a.dir), a.base
    pages = {}
    for f in sorted(root.rglob("*.htm*")):
        h = Head()
        h.feed(f.read_text(encoding="utf-8", errors="replace"))
        pages[norm(page_url(f, root, base))] = (f, h)
    errors, warns = [], []
    for url, (f, h) in pages.items():
        name = f.relative_to(root).as_posix()
        if not h.alts:
            continue  # page without language versions
        if not h.lang:
            errors.append(f"{name}: <html> has no lang attribute")
        bad = [l for l in h.alts if not TAG.match(l)]
        if bad:
            errors.append(f"{name}: invalid hreflang codes {bad}")
        if "x-default" not in h.alts:
            warns.append(f"{name}: no x-default alternate")
        self_langs = [l for l, u in h.alts.items() if norm(u) == url and l != "x-default"]
        if not self_langs:
            errors.append(f"{name}: does not list itself among its alternates")
        elif h.lang and h.lang not in self_langs:
            errors.append(f"{name}: html lang='{h.lang}' but this page is listed as {self_langs}")
        rtl = (h.lang or "").split("-")[0] in {"ar", "he", "fa", "ur", "ps", "sd", "ug", "yi", "dv", "ckb"}
        if rtl and (h.dir or "").lower() != "rtl":
            errors.append(f"{name}: right-to-left language without dir=\"rtl\"")
        if h.canonical and norm(h.canonical) != url:
            warns.append(f"{name}: canonical points to another URL ({h.canonical}); hreflang is then ignored")
        for l, u in h.alts.items():
            if l == "x-default":
                continue
            other = pages.get(norm(u))
            if not other:
                if norm(u).startswith(norm(base)):
                    errors.append(f"{name}: alternate {l} -> {u} has no page in {root}")
                continue
            if url not in {norm(x) for x in other[1].alts.values()}:
                errors.append(f"{name}: {l} version {u} does not link back (hreflang must be reciprocal)")
    for line in errors:
        print("ERROR", line)
    for line in warns:
        print("warn ", line)
    print(f"\nChecked {len(pages)} pages: {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--base", required=True)
    g.add_argument("--langs", required=True)
    g.add_argument("--default")
    g.add_argument("--paths", help="comma list of page paths (default /)")
    g.add_argument("--sitemap", help="write a sitemap.xml with xhtml:link alternates here")
    g.add_argument("--default-at-root", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--dir", required=True)
    c.add_argument("--base", required=True)
    a = ap.parse_args()
    sys.exit(generate(a) if a.cmd == "generate" else check(a))


if __name__ == "__main__":
    main()
