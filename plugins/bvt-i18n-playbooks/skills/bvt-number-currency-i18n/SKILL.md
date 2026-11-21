---
name: bvt-number-currency-i18n
description: Formats numbers, token amounts and fiat currency correctly per locale in crypto apps, covering the Intl API, Hermes gaps on React Native, Indian lakh and crore grouping, native digit systems and bigint token amounts. Use when displaying any balance, price, fee, percentage or fiat value.
---

# Numbers & Currency Localization

## The Hermes trap — check this first
React Native's Hermes engine ships **partial** `Intl` support. Constructors and options that work in Node and in a browser can throw or silently misformat on device — currency formatting on Android has produced `RangeError: Invalid number value` from Hermes' ICU bridge.

Therefore:
1. **Never trust `Intl` on RN without an on-device test.** A CI test in Node proves nothing.
2. Polyfill with FormatJS where needed, importing the polyfill **and the locale data for every shipped locale**:
   `@formatjs/intl-getcanonicallocales/polyfill` → `intl-locale` → `intl-pluralrules` → `intl-numberformat` → `intl-datetimeformat` (+ `locale-data/<lang>` for each).
3. Polyfill imports go at the very top of `index.js`, alongside `react-native-get-random-values`, before anything else.
4. Locale data is per-language and adds bundle weight — load it dynamically for the selected locale rather than bundling all of them.

## Indian grouping — the one you will get wrong
India does **not** group in thousands.
```js
new Intl.NumberFormat('en-IN').format(1234567)          // 12,34,567   (lakh/crore, 2-2-3)
new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })
  .format(1234567.89)                                   // ₹12,34,567.89
```
Never hand-roll a comma inserter. A rupee amount grouped Western-style reads as wrong by a factor of ten to an Indian user.

## Native digit systems
`hi-IN` does **not** produce Devanagari digits by default — it returns `1,23,456`. Nor does bare `ar`. You must request the numbering system explicitly:
```js
new Intl.NumberFormat('hi-IN-u-nu-deva').format(1234)   // १,२३४
new Intl.NumberFormat('ar-EG').format(123456)           // Eastern Arabic digits
```
**Default to Western digits for financial values even in Hindi and Arabic UI.** Most Indian and Gulf users read amounts in Western digits, and mixing digit systems between the app and a bank statement or block explorer causes verification errors. Make native digits an explicit opt-in if you offer it at all.

## Token amounts are bigint, not numbers
```ts
// amount: bigint (wei), decimals: number from the token registry
const asDecimalString = formatUnits(amount, decimals);   // exact, no float
display(new Intl.NumberFormat(locale, { maximumFractionDigits: 8 }).format(Number(asDecimalString)));
```
- Convert to a float **only at the final display step**, never for storage, comparison or arithmetic.
- For very large or very precise values, format the decimal string manually against the locale's separators rather than round-tripping through `Number`.
- **Never abbreviate on a confirmation screen.** "1.2M USDT" is a bug where the user is authorizing a transfer.

## Currency vs token
`style: 'currency'` is for **fiat** (INR, USD). Token amounts are formatted as decimals with the ticker appended as a literal — `Intl` has no currency code for tokens like USDT or ETH, and forcing one produces nonsense.

**A rupee-pegged stablecoin displays in ₹ and a dollar-pegged one in $, regardless of the user's locale.** The token defines the unit; the locale defines the separators. Never swap the symbol based on device region.

## Percentages and prices
Use `style: 'percent'` with explicit fraction digits. Price precision comes from the market's tick size, not from the locale.
