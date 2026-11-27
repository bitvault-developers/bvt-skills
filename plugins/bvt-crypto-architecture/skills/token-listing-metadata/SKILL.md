---
name: token-listing-metadata
description: Prepares token metadata and listing submissions. Use when producing a token list conforming to the Uniswap schema, validating and versioning it, generating logo assets, or assembling a CoinGecko or CoinMarketCap listing application. A name, symbol, logo or decimals change is a patch version; an address or chain id change is a major version treated as a removal plus an addition.
---

# Token Listing & Metadata

## Token list (Uniswap schema)
Schema id: `https://uniswap.org/tokenlist.schema.json`. Validate in CI with `ajv` — an invalid list fails silently in some consumers and loudly in others.

Required per token: `chainId`, `address` (checksummed), `name`, `symbol`, `decimals`. Optional: `logoURI`, `tags`, `extensions`.

## Versioning (semver, and the rule people get wrong)
- **patch** — name, symbol, logo or decimals changed
- **minor** — token added
- **major** — token **removed**, or an **address or chainId changed** (treated as a remove plus an add)

Never silently repoint an address in place. A consumer that cached the old entry now holds a wrong mapping with no signal that anything changed.

## Logos
PNG, **200×200**, transparent background, square, centred, no padding beyond the glyph. Source assets that arrive as JPEG on white require background removal every time — automate it and check the output, since edge halos survive naive thresholding. Serve over HTTPS from a stable path; a changing logo URL is a patch bump.

For a large token set, generate deterministically: `logos/<chainId>/<checksummed-address>.png`, and fail the build on any missing file rather than shipping a list with blank icons.

## CoinGecko / CoinMarketCap submission
Both expect: verified contract on an explorer · working website with a clear description · public team or a credible presence · a **live public API** exposing price, 24h volume and order book depth for the trading venue · circulating supply methodology · social/community links.

Reality: review typically runs **~2–6 weeks**; a token remains **"Untracked"** until it trades on a venue the aggregator already tracks. Listing your own exchange with the aggregator is therefore usually the prerequisite step, not the token listing itself.

## Metadata gaps to close before submitting
A factory-generated set often has no `coingeckoId` and no `logoURI`. Decide the standin explicitly, record it, and do not let a placeholder ship as if it were real metadata.
