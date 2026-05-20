# Research Notes — Momentum Signal Analysis

## Objective

Investigate whether short-term price slope (momentum) in order book data has predictive value for future returns — supporting operational decisions around execution timing and strategy tuning.

## Methodology

- **Data**: Raw tick-level order book snapshots (`bid`, `ask`) at millisecond resolution across multiple assets
- **Signal**: Linear regression slope of `ln(mid)` over rolling windows (2000ms, 5000ms)
- **Output**: Slope expressed in bps/second, binned into deciles
- **Validation**: Average forward return and win rate measured at 5s and 10s horizons per decile

## Key findings

- Price slope shows directional signal at short horizons in certain market regimes
- 5000ms window showed stronger decile separation than 2000ms on the tested data
- Results vary significantly by asset and market conditions — consistent with known microstructure literature

## Operational relevance

This research was used to better understand execution timing and market microstructure behavior in the context of real-time trading operations — not as a standalone strategy, but as an analytical layer supporting operational awareness.

## Tools

Python — pandas, numpy, openpyxl, matplotlib
