---
name: bvt-charts-and-market-viz
description: Implements charts and market data visualization for crypto apps including candlestick charts, portfolio and sparkline views, and performant rendering on mobile. Use when adding a price chart, portfolio allocation view, historical performance graph, or any data visualization that updates in real time.
---

# Charts & Market Visualization

## Renderer choice
| Need | Use |
|---|---|
| candlesticks, high-frequency updates, mobile | Skia (`@shopify/react-native-skia`) |
| simple sparklines / small series | `react-native-svg` (fine below ~200 points) |
| web/desktop shell | lightweight-charts or a canvas renderer |

**Do not render a candlestick chart with per-candle SVG nodes.** It works in a demo and janks at 500 candles on a mid-range Android.

## Data handling
- Candles bucketed by **open time**, UTC-aligned. An interval with no trades carries the previous close with zero volume — do not leave a gap.
- **A closed candle is immutable.** Corrections arrive as new events; never mutate history in place, or the chart flickers and the user loses trust in it.
- Only the in-progress candle updates live; throttle its redraw (~4–10 fps is plenty).
- Downsample before rendering: LTTB (largest-triangle-three-buckets) preserves visual shape far better than naive decimation for long ranges.
- Keep the full series out of React state — hold it in a ref/store and drive redraws imperatively.

## Precision
Prices and volumes arrive as strings/bigints. Convert to float **only at the pixel-mapping step**, never for storage, comparison, or display. Axis labels format from the source value, not the plotted float.

## Interaction
- Crosshair and tooltip driven by Reanimated on the UI thread, not JS state per touch move.
- Pinch-zoom and pan on the time axis; clamp to loaded range and lazy-load older candles at the edge.
- Haptic tick on crosshair snap is a nice touch; make it respect reduce-motion/haptic settings.

## Portfolio views
- Allocation by **value**, with a clearly labelled "other" bucket — a 900-token pie chart is unreadable.
- Historical portfolio value needs a stated methodology (which price source, which timestamp) shown in the UI. An unexplained performance number in a wallet is a support ticket.
- Never annualize or project a return. Show what happened, not what might.

## Accessibility
Every chart carries a text summary (`accessibilityLabel`) with the range, open, close and change. A chart with no screen-reader equivalent is invisible to part of your users.
