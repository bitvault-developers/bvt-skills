---
name: bvt-i18n-a11y
description: Implements localization and accessibility for BitVault apps, covering Hindi and other Indian languages, number and currency formatting, screen reader support and dynamic type. Use when adding user facing strings, formatting balances or fiat amounts, adding screen reader labels, or supporting larger text sizes and higher contrast.
---

# Localization & Accessibility

## Localization
- `i18next` + `expo-localization`. Namespaced keys, no hardcoded user-facing strings anywhere — enforce with an ESLint rule flagging string literals in JSX.
- Priority languages for this market: **English, Hindi (Devanagari)**, then Marathi, Gujarati, Tamil, Telugu, Bengali, Kannada.
- Devanagari renders taller than Latin. **Test every screen at the longest translation** — German and Hindi both break layouts built to English width. Never fix by truncating a balance.
- Pluralization through i18next plural rules, not string concatenation.
- Dates and relative times through `Intl`, locale-aware.

## Numbers and money — the part that goes wrong
- Balances format via `Intl.NumberFormat` with the token's decimals, **from a bigint**, never from a float.
- **Indian digit grouping is not thousands-grouping.** ₹12,34,567 (lakh/crore), not ₹1,234,567. `Intl.NumberFormat('en-IN')` handles this — do not hand-roll a comma inserter.
- BRINR displays as ₹-denominated; BRUSD as $-denominated. Never swap the symbol based on device locale — the token defines the unit, not the user's region.
- Never abbreviate an amount on a confirmation screen. "1.2M BVT" on a send confirmation is a bug.

## Accessibility
- Every interactive element: `accessibilityLabel`, `accessibilityRole`, and `accessibilityState` where it toggles.
- **Amounts must be read in full by the screen reader.** Provide an `accessibilityLabel` that spells the amount and token even when the visual is truncated — a screen-reader user confirming a transfer must hear the whole number.
- Addresses: label the full address, or read it in grouped chunks. A truncated `0x12…ab` is useless aloud.
- Touch targets ≥ 44×44pt. Signing buttons larger.
- Support Dynamic Type / font scaling; no fixed pixel heights on text containers.
- Contrast ≥ 4.5:1 for text. Never encode state by colour alone — a red/green amount needs a sign or an icon too.
- Seed-phrase screens stay accessible: the words must be readable by a screen reader, but the screen still blocks capture and blurs on background.

## Testing
VoiceOver (iOS) and TalkBack (Android) on the send and backup flows at minimum. Run the app at 200% font scale and confirm nothing critical is clipped.
