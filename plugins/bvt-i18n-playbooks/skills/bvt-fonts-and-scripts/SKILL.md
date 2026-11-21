---
name: bvt-fonts-and-scripts
description: Selects, loads and tests fonts for the scripts an app supports including Devanagari, Arabic, and CJK, covering complex script shaping, fallback chains, bundle size and tabular figures. Use when adding a language whose script the current font does not cover, fixing missing or broken glyphs, or reducing font payload.
---

# Fonts & Complex Scripts

## Coverage first
Most Latin UI fonts cover **no** Devanagari, Arabic or CJK. A missing glyph renders as tofu (□) or silently falls back to a system font that does not match your design — usually noticed only after launch, by users.

Plan a family per script group:
- Latin/Cyrillic/Greek: the base UI family
- Devanagari (Hindi, Marathi): a matching Devanagari companion
- Arabic/Urdu: an Arabic companion with proper contextual shaping
- CJK: a CJK family — these are **large** (multiple MB per weight)

Prefer a superfamily designed for cross-script harmony so the app does not look like three different products.

## Do not bundle everything
CJK fonts alone can exceed the whole JS bundle. Strategy:
- **Rely on the platform font** for CJK and Arabic where the design allows — iOS and Android ship good ones, and they update with the OS.
- Bundle **only** the scripts where the brand font matters and the file is small (Latin, Devanagari).
- Load script-specific fonts **dynamically when that locale is selected**, not at startup.
- Subset aggressively: strip unused weights, styles and glyph ranges.

## Complex script correctness
Devanagari and Arabic are **shaped**, not just mapped: conjuncts, matras, ligatures, and contextual letter forms. Consequences:
- Never letter-space, force-uppercase, or apply per-character animation to these scripts — it destroys shaping.
- Do not measure text by character count; measure rendered width.
- Custom text rendering (Skia, canvas) must go through the platform shaper. A hand-rolled glyph renderer will produce broken Devanagari.
- Test with real strings containing conjuncts (क्ष, त्र, ज्ञ) and Arabic initial/medial/final forms, not lorem ipsum.

## Legacy encodings
Indian content sometimes arrives in legacy non-Unicode fonts (Kruti Dev and similar) that map Devanagari glyphs onto ASCII positions. **Never accept these into the pipeline** — convert to Unicode at the boundary. Non-Unicode text is unsearchable, unsortable, and breaks the moment the font is absent.

## Numerals
Use **tabular (monospaced) figures** for balances, order books and any numeric column so digits align. Check that the tabular feature exists in the weight you shipped — it often does not in a light weight.

## Fallback chain
Define an explicit chain per locale and verify on a **real device**: emulators carry a different font set than shipping phones, and low-end Android devices in the Indian market frequently lack fonts the emulator has.

## Test set
Render one screen per script with: the longest translation, a conjunct-heavy string, a number, an address, and an emoji. That single screen catches most font defects.
