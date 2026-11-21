---
name: bvt-text-expansion-layout
description: Designs interfaces that survive text expansion and script height differences across languages. Use when building a screen, setting a button width, choosing a truncation strategy, or fixing a layout that breaks in German, Hindi, Arabic or Japanese.
---

# Text Expansion & Layout

## Budget for growth
Rough expansion from English source text:
| Target | Typical growth |
|---|---|
| German, Russian, Finnish | +30–40% |
| French, Spanish, Portuguese, Italian | +20–30% |
| Hindi and other Indic | +15–25%, **and noticeably taller** |
| Arabic | +20–25%, taller, RTL |
| Japanese, Chinese, Korean | −20–40% shorter, but **taller line boxes** |

Short strings expand worst: a 4-character English button label can triple.

## Rules
- **Never fix a text container's height.** Height is content-driven, always.
- Buttons size to content with a sensible minimum; they do not clip.
- Avoid side-by-side equal-width buttons for long labels — stack on narrow screens.
- Indic and Arabic scripts have taller ascenders/descenders and need more line-height than Latin. Set line-height as a **multiplier**, never a fixed pixel value.
- Tab bars and segmented controls are the first thing to break. Prefer icons with short labels, and test at the longest translation.
- Test at **200% font scale** as well as the longest translation — expansion and Dynamic Type compound.

## Truncation policy
| Content | Policy |
|---|---|
| descriptive labels, list subtitles | ellipsize, full value available on tap |
| addresses | middle-truncate (`0x1234…abcd`), full value in the a11y label |
| **amounts and balances** | **never truncate on a confirmation or signing screen** |
| button labels | never truncate — resize the design instead |

If a translated label cannot fit, the fix is the layout or a shorter source string. **It is never a shorter translation that drops meaning**, and it is never a smaller font on a financial value.

## Pseudolocalization catches this before translators do
Run the app in a pseudo-locale that expands every string ~40% and wraps it in brackets with accented characters:
`[Ĉöñƒîŕɱ ţŕàñšàçţîöñ————]`
Anything unbracketed is a hardcoded string; anything clipped is a layout bug. This finds both classes of defect with zero translation cost. Wire it as a build flag and run it every release.

## Numbers are not immune
`12,34,567.89` (Indian grouping) is wider than `1,234,567.89`. Currency symbols vary in width. Right-align numeric columns and use tabular figures so digits line up regardless of locale.
