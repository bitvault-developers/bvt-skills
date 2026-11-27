---
name: market-data-feeds
description: Builds exchange market data distribution. Use when publishing order book snapshots and incremental depth updates, trade streams, candlesticks and tickers, handling sequence numbers and gap recovery, fanning out to many WebSocket subscribers, or integrating a charting library. Clients must be able to detect a missed sequence and resynchronise.
---

# Market Data Feeds

## Depth protocol (the part clients get wrong)
Publish a **snapshot** plus **incremental updates**, each carrying `U` (first update id) and `u` (last update id).

Documented client procedure:
1. Buffer the incremental stream.
2. Fetch a snapshot with `lastUpdateId`.
3. Discard buffered events where `u <= lastUpdateId`.
4. The first applied event must satisfy `U <= lastUpdateId + 1 <= u`.
5. Thereafter each event's `U` must equal the previous `u + 1` — **if not, discard the book and restart from step 1.**

Publish this procedure in your docs verbatim. Without it, every integrator builds a subtly wrong book.

A zero quantity at a price means **remove the level**, not "level with zero size".

## Streams
- `trade` — id, price, qty, side, timestamp
- `ticker` — 24h rolling stats; throttle to ~1s
- `kline` — send the in-progress candle on an interval plus a final closed candle flagged as closed
- `depth` — snapshot + increments as above

Candle rules: bucket by open time, UTC aligned; an interval with no trades carries the previous close with zero volume; **never revise a closed candle** — a correction is a new event.

## Fanout
- One engine → one publisher → N subscriber connections. The engine never writes to sockets.
- Per-connection outbound queue with a bounded size; **slow consumer gets disconnected**, not backpressured into the publisher.
- Coalesce updates per tick for throttled streams rather than sending every change.
- Heartbeat/ping every ~20–30s; drop on missed pong.
- Subscribe/unsubscribe per topic on one connection; cap topics per connection.

## Integrity
Sequence numbers on every stream. Publish the current sequence in the snapshot. Monitor and alert on publisher lag behind the engine — market data lag is a trading-fairness issue, not a cosmetic one.
