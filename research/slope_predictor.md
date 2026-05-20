# Slope Predictor — Research Summary

**Goal**: Find a model that predicts market direction using only price data.  
**Data**: 50 million tick-level samples across BTCUSDT, ETHUSDT, BNBUSDT (27 files, Feb–Mar 2026).

---

## Research Journey

### Phase 1 — HFT Signal Research

Tested 6 models on tick-level data to find a short-term directional edge:

| Model | Accuracy | Verdict |
|---|---|---|
| Mean Reversion | **85–89%** | Strong signal |
| MA Crossover (fast) | 63% | Weak |
| Momentum | 62% | Weak |
| Savitzky-Golay Slope | 54% | Weak |
| RSI-like | 50% | No edge |

Mean reversion hit **89% accuracy** when price was within 0.01% of its moving average.

### The Problem

```
Expected price move:   0.01 – 0.05%
Binance round-trip fee: 0.20%
──────────────────────────────────
Net result:            LOSS
```

High accuracy, but the moves were too small to cover transaction costs.
**89% accuracy is statistically real — it's just not profitable.**

---

## Pivot — Slower Timeframes

**New hypothesis**: If HFT moves are too small, find a timeframe where moves exceed fees.

| Timeframe | Typical Move | vs Fees (0.2%) | Viable? |
|---|---|---|---|
| Milliseconds | 0.01% | 20× smaller | No |
| Minutes | 0.05% | 4× smaller | No |
| 15–30 min bars | 0.30–1.00% | 2–5× larger | **Yes** |

### MA Crossover on 15-Minute Bars

| Symbol | Win Rate | Net Profit/Trade |
|---|---|---|
| BNBUSDT | 73.3% | +0.52% |
| BNBUSDT (30min) | 66.7% | +0.42% |
| ETHUSDT | 55.3% | +0.14% |

Profitable after fees. Needs more data to validate at scale.

---

## Key Takeaways

1. **Accuracy ≠ profitability** — 89% accuracy meant nothing with moves smaller than fees
2. **Fees are a product constraint** — understanding the cost structure changed the entire research direction
3. **Pivoting is the right call** — when the HFT path hit a hard wall, moving to slower timeframes found real alpha
4. **Honest documentation matters** — knowing what doesn't work is as valuable as knowing what does

---

*Full methodology and code available on request.*
