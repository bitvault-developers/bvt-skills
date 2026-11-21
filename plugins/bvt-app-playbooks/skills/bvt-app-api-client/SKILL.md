---
name: bvt-app-api-client
description: Designs typed client code for BitVault backend and exchange APIs including request signing, idempotency, pagination, error taxonomy and response validation. Use when calling the BVTEx trading API, the subscription or profile backend, or any BitVault HTTP or websocket service from an app shell.
---

# App API Client

## Generate, don't hand-write
Derive the client from the API's OpenAPI/schema where one exists; otherwise define request/response schemas with **Zod** and parse every response. **Never cast an API response with `as`** — a shape change then fails silently at the point of use instead of loudly at the boundary.

Client code lives in `packages/rpc` (chain) or `packages/business` (services) — never in a shell.

## Auth
- HMAC-SHA256 over a canonical string: `timestamp + method + path + body`.
- Include a `recvWindow`; reject responses to requests whose timestamp has aged out.
- API secrets live in secure storage, never in a state store or a config file. On mobile, an exchange API key is a secret with the same handling as a seed.
- Scope keys: read · trade · withdraw. **Withdraw scope is never enabled by default** and requires explicit re-authentication to turn on.

## Idempotency
Every mutating call (place order, subscribe, transfer) carries a **client-generated id**. The same id resubmitted returns the original result. Mobile networks time out constantly; without this, a retry double-fills an order or double-charges a subscription.

Generate the id **before** the first attempt and reuse it across retries — generating it inside the retry loop defeats the entire mechanism.

## Errors
Map to a tagged union with a stable `code`, and branch on the code, never on the message string. Distinguish: network · auth · rate-limited · validation · insufficient-balance · market-halted · server. Only the first three are retryable; a validation error retried is just noise.

Respect `429` + `Retry-After` and back off globally, not per-call.

## Pagination
Cursor-based (`fromId` / `startTime` + `limit`). Offset pagination duplicates and skips rows under concurrent inserts — visible to users as a missing trade in their history.

## Subscription flow (on-chain, not an API)
The 10 BRUSD/month subscription is a **chain interaction**, not an HTTP call: `BRUSD.approve(subscriptionContract, amount)` then `subscribe()`. Show both steps in the UI — a user who approves and then backgrounds the app has not subscribed, and must be able to resume at step two. Never re-request approval if allowance is already sufficient.

## Websocket
Same discipline as the REST client: typed events parsed at the boundary, explicit reconnect, sequence tracking (see `bvt-exchange-client-ui`).
