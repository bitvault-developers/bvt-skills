---
name: oracle-integration
description: Integrates and hardens price and foreign exchange oracles for crypto protocols. Use when consuming Chainlink feeds, building or repairing TWAP sources, adding staleness and round-completeness checks, handling multi-source aggregation and outlier rejection, or assessing oracle manipulation risk in a contract under review.
---

# Oracle Integration

## Chainlink read — the minimum safe pattern
```solidity
(uint80 roundId, int256 answer, , uint256 updatedAt, uint80 answeredInRound) = feed.latestRoundData();
require(answer > 0,                    "bad answer");
require(updatedAt != 0,                "incomplete round");
require(answeredInRound >= roundId,    "stale round");
require(block.timestamp - updatedAt <= MAX_AGE, "stale price");
```
`MAX_AGE` must be set per feed from that feed's documented heartbeat — not a single global constant.

Also: read `decimals()` from the feed; never hardcode 8 or 18.

## Failure policy
Decide explicitly, per consumer, what happens when the feed is unusable:
- **halt** the dependent operation (correct for minting and redemption), or
- **fall back** to a last-good value with a hard maximum age and a visible degraded state.

Never allow a silent stale read to price a mint.

## TWAP / multi-source
- Aggregate at least 3 sources; take the median, not the mean.
- Reject any source deviating beyond a fixed band from the median.
- Bound the per-update move; a change beyond the bound is treated as a fault, not a price.
- Record which sources contributed to each update so a bad print can be attributed.
- Window length is a security parameter: short windows are manipulable, long windows lag a real move.

## Manipulation classes to check in review
- Spot price read from a DEX pool with shallow liquidity (flash-loan manipulable)
- Single-source dependency with no fallback
- Missing staleness check (the most common finding)
- Price used both to mint and to value collateral, with no bound on divergence
- Rounding that always favours the caller
