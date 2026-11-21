---
name: bvt-datetime-i18n
description: Formats dates, times and relative times per locale in crypto apps, covering time zones, exchange timestamps, candle labels and calendar systems. Use when displaying a transaction time, order history, chart axis, staking period or any time based value.
---

# Date & Time Localization

## Always store UTC, always display local
Every timestamp in the ledger, the chain and the API is UTC. Conversion happens at the render edge only. A timestamp stored in local time is unrecoverable once the user travels.

## Formatting
```js
new Intl.DateTimeFormat(locale, { dateStyle: 'medium', timeStyle: 'short' }).format(d)
```
Never hand-assemble `DD/MM/YYYY` — the order, separator, month name and 12/24-hour convention are all locale-dependent, and `MM/DD` vs `DD/MM` is genuinely ambiguous to the user for half the month.

On React Native, `Intl.DateTimeFormat` is subject to the same **Hermes gaps** as number formatting — polyfill with `@formatjs/intl-datetimeformat` plus locale data plus a timezone dataset (`add-all-tz` is large; add only the zones you need if size matters). Hermes has also returned `GMT-7` where a browser returns `MST` for `timeZoneName: 'short'` — do not rely on short zone names for anything the user must match.

## Relative time
```js
new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-2, 'hour')  // "2 hours ago"
```
`numeric: 'auto'` gives "yesterday" instead of "1 day ago" where the language has it. Never build relative time by string concatenation — plural forms and word order differ.

Relative time is right for transaction history. It is **wrong** for anything the user must reconcile against another system: an order fill, a tax statement, a withdrawal record. Show the absolute timestamp there, with the timezone.

## Exchange and chart timestamps
- Candle buckets are UTC-aligned. Axis labels format in the user's locale but the **bucket boundary never moves** — a chart that shifts candles by timezone is wrong.
- Order and fill timestamps show to the second, with an explicit timezone indicator. A trader disputing a fill needs an unambiguous time.
- Offer a UTC display toggle in the exchange client. Traders expect it.

## Calendars
Some locales default to a non-Gregorian calendar (`ar-SA` → Islamic, `fa-IR` → Persian, `th-TH` → Buddhist era). For financial records, **force `calendar: 'gregory'`** on anything that must match a statement, a block explorer or a tax filing, and let purely cosmetic dates follow the locale.

## Durations
Staking periods, lock-ups and timelock delays ("48 hours") are messages with plural arguments, not concatenated numbers. `{hours, plural, one {# hour} other {# hours}}`.

## Never
- Assume a week starts on Monday (or Sunday).
- Use a locale's default calendar for a tax or compliance export.
- Display a time without a zone on a record the user may dispute.
