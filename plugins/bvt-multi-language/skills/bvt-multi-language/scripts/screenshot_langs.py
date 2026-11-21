#!/usr/bin/env python3
"""Open the app in every language, take screenshots and catch translation bugs a person would miss.

  python screenshot_langs.py --url "http://localhost:3000/{lang}/" --langs en,ar,hi,de,ja,en-XA \\
      --base src/locales/en.json --out screenshots/
  python screenshot_langs.py --url "http://localhost:5173/?lng={lang}" --langs en,ar --mobile

Per language it reports: raw translation keys on screen (home.title), unfilled placeholders ({name}, {{count}}),
a wrong <html lang>, a right-to-left language without dir="rtl", JavaScript errors, and for the pseudo-locale
(en-XA, from check_locales.py pseudo) text that was NOT pseudo-translated, which is hard-coded text.
Needs Playwright: pip install playwright && playwright install chromium. Exit code 1 when anything is found.
"""
import argparse, json, re, sys
from pathlib import Path

RTL = {"ar", "he", "fa", "ur", "ps", "sd", "ug", "yi", "dv", "ckb", "ks"}
PLACEHOLDER = re.compile(r"\{\{\s*[A-Za-z_][\w.]*\s*\}\}|\{[A-Za-z_]\w*\}|%(?:\d+\$)?[sd]\b")


def flat_keys(path):
    if not path:
        return set()
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    def walk(d, prefix=""):
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                yield from walk(v, key)
            elif not k.startswith("@"):
                yield key
    return {k for k in walk(data) if "." in k or "_" in k}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", required=True, help="URL template with {lang}")
    ap.add_argument("--langs", required=True)
    ap.add_argument("--base", help="base locale file; its keys are looked for on screen")
    ap.add_argument("--out", default="screenshots")
    ap.add_argument("--mobile", action="store_true", help="iPhone-sized viewport")
    ap.add_argument("--wait", type=int, default=800, help="ms to wait after load for client rendering")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright is missing: pip install playwright && playwright install chromium")

    keys = flat_keys(a.base)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    total = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 390, "height": 844} if a.mobile else {"width": 1366, "height": 900},
                                  device_scale_factor=1)
        for lang in [l.strip() for l in a.langs.split(",") if l.strip()]:
            page = ctx.new_page()
            js_errors = []
            page.on("pageerror", lambda e: js_errors.append(str(e)))
            page.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)
            problems = []
            try:
                page.goto(a.url.format(lang=lang), wait_until="networkidle", timeout=30000)
            except Exception as e:
                problems.append(f"page did not load: {e}")
            page.wait_for_timeout(a.wait)
            info = page.evaluate("""() => {
                const texts = [];
                const w = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT);
                while (w.nextNode()) {
                  const n = w.currentNode, el = n.parentElement;
                  if (!el || ['SCRIPT','STYLE','NOSCRIPT','CODE','PRE'].includes(el.tagName)) continue;
                  const s = n.textContent.trim();
                  if (s && el.offsetParent !== null) texts.push(s);
                }
                document.querySelectorAll('[placeholder],[title],[aria-label],[alt]').forEach(el => {
                  for (const a of ['placeholder','title','aria-label','alt']) { const v = el.getAttribute(a); if (v) texts.push(v.trim()); }
                });
                return {lang: document.documentElement.lang, dir: document.documentElement.dir || getComputedStyle(document.documentElement).direction, texts};
            }""")
            texts = info["texts"]
            if not lang.endswith("XA") and info["lang"].lower() != lang.lower() and not info["lang"].lower().startswith(lang.split("-")[0].lower()):
                problems.append(f"<html lang> is '{info['lang']}'")
            if lang.split("-")[0] in RTL and info["dir"] != "rtl":
                problems.append("right-to-left language but the page is not dir=rtl")
            raw = sorted({t for t in texts if t in keys})
            if raw:
                problems.append(f"raw keys on screen: {raw[:8]}")
            ph = sorted({m.group(0) for t in texts for m in PLACEHOLDER.finditer(t)})
            if ph:
                problems.append(f"unfilled placeholders: {ph[:8]}")
            if lang.endswith("XA"):  # pseudo-locale: every translated string is wrapped in [ ... ~~~ ]
                plain = sorted({t for t in texts if re.search(r"[A-Za-z]{3,}", t) and not t.startswith("[")
                                and not t.endswith("]")})
                if plain:
                    problems.append(f"{len(plain)} texts not pseudo-translated (hard-coded?): {plain[:6]}")
            if js_errors:
                problems.append(f"JavaScript errors: {js_errors[:3]}")
            shot = out / f"{lang}.png"
            page.screenshot(path=str(shot), full_page=True)
            print(f"{lang:>8}: {'OK' if not problems else str(len(problems)) + ' problem(s)'}  -> {shot}")
            for pr in problems:
                print(f"{'':>10}- {pr}")
            total += len(problems)
            page.close()
        browser.close()
    print(f"\n{total} problems. Look at the screenshots too: an RTL language, a long-text language (de), "
          "a complex script (hi/th) and the pseudo-locale.")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
