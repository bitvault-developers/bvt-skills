---
name: bvt-exchange-client-ui
description: Builds a crypto exchange client interface including real time order book rendering, websocket reconnection with sequence gap recovery, order entry, and application background and foreground handling. Use for order book, trade feed, depth, order ticket or any live market data code in the mobile, desktop or web client.
---

# Exchange Client UI

## Order book rendering
- Fixed row count (e.g. 20 levels a side); **never render an unbounded book.** Aggregate the tail.
- Keep the book in a **ref or an external store, not React state.** A state update per depth message re-renders at message rate and destroys the frame budget. Render on an interval (~10 fps) from the current snapshot.
- Recycled rows keyed by **price level**, not array index, so a level insert doesn't repaint the whole ladder.
- Depth bars drawn as a scaled background width, not a nested view tree per row.
- Price/size formatting from bigint with the market's tick and lot precision — never a float.

## The websocket contract (implement exactly)
1. Buffer incremental depth events.
2. Fetch the snapshot with `lastUpdateId`.
3. Drop buffered events where `u <= lastUpdateId`.
4. First applied event must satisfy `U <= lastUpdateId + 1 <= u`.
5. Thereafter each event's `U` must equal the previous `u + 1`.
6. **On any gap: discard the local book and restart from step 1.**

A gap is not recoverable by patching. Silently continuing after a missed sequence produces a book that is wrong in a way the user cannot see. Surface a brief "resyncing" state rather than showing stale depth as live.

Zero quantity at a price means **remove the level**.

## Reconnection
Exponential backoff with jitter, capped. On reconnect: resubscribe all topics, then resnapshot every book — never assume the book survived. Heartbeat/ping ~20–30s; treat a missed pong as a disconnect. Show connection state in the UI; a frozen book that looks live is worse than a visible "disconnected".

## Background / foreground
On background: close or suspend market data streams (battery, and the data is stale on return anyway). On foreground: reconnect, resnapshot, and **clear any displayed price older than a few seconds** before showing it. Never let a chart or ticker render pre-background data as current.

## Order entry
- Client order id on every placement — **idempotent**, so a retry after a timeout cannot double-fill.
- Show the full effect before submit: pair, side, type, price, quantity, estimated fee, total.
- Market orders require slippage protection or a price band; never submit an unbounded market order from mobile.
- Optimistic UI for *acknowledgement*, never for a fill. A fill is only real when the exchange says so.
- Cancel is idempotent — cancelling an already-cancelled order shows current state, not an error.

## Charts
A canvas/Skia-based renderer, not a DOM/SVG chart, on mobile. Never revise a closed candle — a correction arrives as a new event.
