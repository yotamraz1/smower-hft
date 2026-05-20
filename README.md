# smower-hft — Analytics & Research

Analytics and quantitative research scripts from a live automated trading platform.

---

## Contents

### `run_slope_research.py` — Momentum Signal Research

Investigates whether short-term price slope in order book data predicts future returns.

**What it does:**
- Ingests raw tick data (`timestamp`, `bid`, `ask`) at millisecond resolution
- Computes mid price: `mid = (bid + ask) / 2`
- Fits a linear regression of `ln(mid)` vs. time over a rolling window
- Outputs slope in **bps/second** as a momentum signal
- Computes forward returns at configurable horizons
- Decile analysis: bins by slope, measures average forward return per bucket

```python
# Core slope formula
beta = ((x - x_mean) * (y - y_mean)).sum() / ((x - x_mean)**2).sum()
slope_bps_per_s = beta * 1000.0 * 10000.0
```

**Usage:**
```bash
# Single file
python3 run_slope_research.py --input data/parsed_BTCUSDT.csv

# Full folder
python3 run_slope_research.py --input data/ --glob "*.csv" --combine \
  --slope-windows-ms 500,2000,5000 \
  --horizons-ms 1000,5000,10000
```

**Output:** per-file features CSV + Excel workbook with decile summary sheets.

---

### `plot_quotes.py` — Order Book Visualization

Reads raw tick data and plots mid price over time — used for visual inspection of market microstructure.

```bash
# Set FILE = "your_data.txt" inside the script, then:
python3 plot_quotes.py
```

---

## Stack

- Python — pandas, numpy, matplotlib
- PostgreSQL (production analytics)
- Linux / AWS

---

*Full project context and performance data: [Notion portfolio]*
