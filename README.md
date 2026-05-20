# execution-analytics

Python-based analytics and visualization workflows for real-time market data, operational monitoring, and execution research.

---

## My Role

This repository reflects hands-on analytical and operational research work within a live real-time trading environment.

My primary involvement focused on analytics, monitoring, operational workflows, and data-driven optimization. Core infrastructure and execution systems were primarily developed by my technical co-founder.

---

## Structure

```
execution-analytics/
├── src/
│   ├── run_slope_research.py   — momentum signal research engine
│   └── plot_quotes.py          — order book visualization
├── outputs/
│   └── charts/                 — generated analysis outputs
├── screenshots/                — dashboards & monitoring visuals
└── notes/
    └── research_findings.md    — methodology & findings
```

---

## `run_slope_research.py` — Momentum Signal Research

Investigates whether short-term price slope in order book data predicts future returns — used to support operational understanding of execution timing and market behavior.

**Methodology:**
1. Ingest raw tick data — `timestamp`, `bid`, `ask` at millisecond resolution
2. Compute mid price: `mid = (bid + ask) / 2`
3. Fit linear regression of `ln(mid)` vs. time over a rolling window
4. Express slope in **bps/second** as a momentum signal
5. Compute forward returns at configurable horizons
6. Decile analysis: bin by slope, measure average forward return per bucket

```python
# Core slope formula
beta = ((x - x_mean) * (y - y_mean)).sum() / ((x - x_mean)**2).sum()
slope_bps_per_s = beta * 1000.0 * 10000.0
```

```bash
# Single file
python3 src/run_slope_research.py --input data/sample.csv

# Full folder with combined output
python3 src/run_slope_research.py --input data/ --glob "*.csv" --combine \
  --slope-windows-ms 500,2000,5000 \
  --horizons-ms 1000,5000,10000
```

---

## `plot_quotes.py` — Order Book Visualization

Reads raw tick data and plots mid price over time — used for visual inspection of market microstructure and regime identification.

---

## Stack

Python · pandas · numpy · matplotlib · PostgreSQL · Linux · AWS
