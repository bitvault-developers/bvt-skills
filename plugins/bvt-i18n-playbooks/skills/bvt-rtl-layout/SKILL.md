---
name: bvt-rtl-layout
description: Implements right to left layout for Arabic, Hebrew, Farsi and Urdu across BitVault mobile, desktop, web and extension shells, covering layout mirroring, icon flipping, bidirectional text isolation and the restart requirement. Use when adding an RTL language, fixing a mirrored layout, or rendering an address or amount inside RTL text.
---

# RTL Layout

## Enabling it
```js
import { I18nManager } from 'react-native';
I18nManager.allowRTL(true);
I18nManager.forceRTL(isRTL);
// then restart — the change does not apply to the running app
```
- **A full app restart is required.** Hot reload will not apply it. Use a restart module and warn the user before switching.
- iOS additionally requires the language to be listed in the app's known localizations; Android requires `android:supportsRTL="true"` on `<application>`. Missing either produces "RTL works on one platform only".
- Set direction **before first render**, in the root layout, alongside i18n init.
- The device locale and the app locale can disagree — an RTL device with the app set to English must force LTR explicitly, or English text renders right-aligned and sliders and toggles run backwards.

## Styles
Replace every directional property:
`marginLeft/Right → marginStart/End` · `paddingLeft/Right → paddingStart/End` · `left/right → start/end` · `textAlign: 'left' → 'start'`.
`flexDirection: 'row'` mirrors automatically once RTL is on. **Absolute positioning does not** — anything positioned absolutely against a flex sibling must be adjusted with `I18nManager.isRTL`.

## Icons
Mirror directional glyphs only: back arrows, next/previous, progress, send/receive arrows, chart direction indicators.
```js
style={{ transform: [{ scaleX: I18nManager.isRTL ? -1 : 1 }] }}
```
**Do not mirror**: logos, coin icons, clocks, checkmarks, media play buttons, or anything containing Latin text or a numeral.

## Bidirectional text — the crypto-specific hazard
An address, hash, ticker or amount is **LTR content inside RTL text**. Without isolation the browser/OS bidi algorithm reorders the surrounding characters and the address renders in a visually different order than it is stored. A user comparing it against a block explorer will see a mismatch — or worse, will not notice one.

Always isolate LTR runs:
- wrap in `\u2066` (LRI) … `\u2069` (PDI), or
- render in a container with `direction: 'ltr'` and `writingDirection: 'ltr'` (RN `Text`) / `unicode-bidi: isolate` (web)

Apply this to: addresses, transaction hashes, seed phrases, derivation paths, chain ids, ticker symbols, and any number rendered next to RTL words. Trailing punctuation next to an isolated run is the classic place it still breaks — test it.

## Gestures and animation
Swipe-to-delete, carousels, back-swipe and slide transitions must reverse. Check every `translateX` animation, chart pan direction, and the order-book side layout (bids/asks swap sides in RTL — decide deliberately whether that is correct for traders and document the choice).

## Desktop, web, extension
Web/Tauri: set `dir="rtl"` on `<html>` and use CSS logical properties (`margin-inline-start`, `inset-inline-start`, `text-align: start`). No restart needed — which means the web build can switch live while the mobile build cannot. Keep the behaviour difference documented rather than trying to make them identical.

## Testing
Every screen gets an RTL screenshot. Layouts that "mostly look fine" in simple views break in nested rows, absolutely positioned badges, and anything with an inline number.
