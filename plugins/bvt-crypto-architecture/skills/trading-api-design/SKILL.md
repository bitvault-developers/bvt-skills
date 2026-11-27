---
name: trading-api-design
description: Designs an exchange public and private trading API. Use when defining REST and WebSocket endpoints, request signing, nonce and timestamp windows, idempotency keys for order placement, rate limiting and weight budgets, error code taxonomy, pagination, or API key permission scopes. Order placement must be idempotent so a client retry cannot double-fill.
---

# Trading API Design

## Surfaces
- **Public REST** — markets, ticker, depth, trades, klines, server time
- **Private REST** — order place/cancel/query, balances, fills, transfers, withdrawals
- **Public WS** — depth, trades, ticker, klines
- **Private WS** — order updates, balance updates, fills

## Authentication
API key + secret. Sign a canonical string: `timestamp + method + path + body`, HMAC-SHA256, hex.
- `recvWindow` (default 5000ms) — reject requests outside it, and reject future timestamps.
- Bind each key to **scopes**: read · trade · withdraw. Withdraw is off by default and requires a separate confirmation to enable.
- Optional IP allowlist per key; require it for withdraw scope.
- Never accept credentials in a query string.

## Idempotency — the one that matters
Every order placement carries a **client order id**. The server stores it with a uniqueness constraint per account.
- Same id resubmitted → return the **original** result, do not place again.
- A client that times out and retries must not double-fill. This is not optional; network retries are certain.

Cancels are naturally idempotent — cancelling an already-cancelled order returns success with the current state, not an error.

## Rate limiting
Weight-based, not request-count-based: heavy endpoints cost more. Publish the weights. Return `X-RateLimit-*` headers and `429` with `Retry-After`. Separate budgets for order-placement and for data reads so a market-data burst cannot lock a user out of cancelling.

## Errors
Stable numeric codes plus a message. Distinguish clearly: bad request · unauthorised · insufficient balance · market halted · rate limited · internal. **Never leak internal state in an error message.** Keep the code list versioned and documented; clients branch on it.

## Pagination
Cursor-based for anything time-ordered (`fromId` / `startTime` + `limit`). Offset pagination breaks under concurrent inserts.

## Versioning and change policy
Prefix with `/api/v1`. Additive changes only within a version. Publish a deprecation window and a changelog; breaking a trading API silently breaks bots holding positions.
