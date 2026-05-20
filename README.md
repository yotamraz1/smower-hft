# execution-analytics

Python-based analytics and visualization workflows for real-time operational monitoring, execution analysis, and market microstructure research.

---

## My Role

My involvement focused primarily on analytics, operational monitoring, workflow optimization, and research-oriented data analysis within a real-time trading environment.

Core low-level infrastructure architecture and execution engine development were primarily led by my technical co-founder.

---

## Operational Context

This work was part of a live automated trading operation running 24/7 across multiple exchanges. The analytics layer supported:

- **Real-time monitoring** — tracking execution health, machine states, and operational KPIs continuously
- **Execution research** — understanding market microstructure behavior to inform operational decisions
- **Anomaly detection** — identifying unexpected patterns in tick data, execution flows, and system behavior
- **Visualization pipelines** — surfacing operational data in formats usable for fast decision-making

---

## Contents

### `src/run_slope_research.py` — Momentum Signal Research

Investigates whether short-term price slope in order book data predicts future returns.

- Ingests raw tick data (`bid`, `ask`) at millisecond resolution
- Fits linear regression of `ln(mid)` vs. time over rolling windows
- Outputs slope in **bps/second** as a momentum signal
- Computes forward returns at configurable horizons
- Decile analysis: bins by slope, measures average forward return per bucket

```python
# Core slope formula
beta = ((x - x_mean) * (y - y_mean)).sum() / ((x - x_mean)**2).sum()
slope_bps_per_s = beta * 1000.0 * 10000.0
```

```bash
python3 src/run_slope_research.py --input data/sample.csv
python3 src/run_slope_research.py --input data/ --glob "*.csv" --combine \
  --slope-windows-ms 500,2000,5000 --horizons-ms 1000,5000,10000
```

### `src/plot_quotes.py` — Order Book Visualization

Reads raw tick data and plots mid price over time — used for visual inspection of market microstructure and regime identification.

---

## Technologies

- **Python** — pandas, numpy, matplotlib, Plotly
- **SQL / PostgreSQL** — production analytics on live trading data
- **Linux / AWS** — production environment, process monitoring, log analysis
- **Excel** — operational reporting and KPI tracking

---

## Screenshots

*See `/screenshots` folder — dashboards, monitoring systems, execution outputs.*

---

## Notes

See `notes/research_findings.md` for methodology and findings from the momentum signal research.
