---
name: bvt-icu-message-format
description: Writes ICU MessageFormat strings for apps including plurals, select, gender, nested arguments, interpolation and escaping. Use when authoring or reviewing any translatable string that contains a variable, a count, a conditional or embedded formatting.
---

# ICU MessageFormat

## Plurals — never hand-roll
```
"tx.confirmations": "{count, plural, one {# confirmation} other {# confirmations}}"
```
`#` inserts the formatted number in the current locale. Do not write `{count} confirmations` and hope.

**English has 2 plural forms. Others do not.** `Intl.PluralRules` defines the categories per language:
- Arabic: `zero`, `one`, `two`, `few`, `many`, `other` — six.
- Russian/Polish/Czech: `one`, `few`, `many`, `other`.
- Hindi: `one`, `other` (but the boundary differs from English).
- Japanese/Chinese/Korean: `other` only.

**Never assume the target has the same forms as the source.** Authoring an English string with only `one`/`other` is correct — the *translator* adds the categories their language needs. Your job is to use `plural`, not to enumerate forms.

## Select and gender
```
"order.status": "{side, select, buy {Buy order} sell {Sell order} other {Order}}"
```
Always include an `other` branch. A missing `other` is a runtime throw, not a fallback.

## Do not concatenate — ever
```
// WRONG — untranslatable; word order differs by language
t('sent') + ' ' + amount + ' ' + t('to') + ' ' + address

// RIGHT — one message, translator controls word order
t('wallet:send.success', { amount, address })
```
Sentence fragments assembled in code are the single most common i18n defect. German, Hindi, Japanese and Arabic all reorder the pieces.

## Interpolation and markup
Keep markup out of the string. Use component interpolation (`<Trans>` / rich-text arguments) so the translator moves the tag with the words:
```
"legal.agree": "I agree to the <terms>Terms</terms> and <privacy>Privacy Policy</privacy>"
```
Never split a sentence around a `<Link>` in JSX — that is concatenation wearing a costume.

## Escaping
- A literal `{` or `}` is escaped with single quotes: `'{'`.
- A literal apostrophe in a message containing arguments must be doubled: `''`. Otherwise ICU treats it as a quote and silently swallows the rest of the segment. This bites French and Italian constantly.
- `#` inside a nested `plural` refers to the innermost count — use the named argument if you mean the outer one.

## Number and date arguments
```
"balance.line": "{amount, number, ::currency/INR} available"
```
Prefer formatting **outside** the message when the value is a token amount (see `bvt-number-currency-i18n`) — ICU number skeletons cannot do bigint token math.

## Every message gets a description
The `description`/context field is what a translator sees instead of your screen. "Confirm" with no context becomes six different words in six languages. Say what it does and where it appears.
