#!/usr/bin/env python3
"""
Slope -> Future Return MVP Research
----------------------------------
Reads one CSV (or a folder of CSVs) with at least:
- timestamp (ms)
- price1, price2  (e.g., bid/ask or ask/bid; we use mid=(price1+price2)/2)

Outputs:
- per-file features CSV
- per-file Excel (features + decile summaries)
- (optional) combined master CSV across all files

Default settings (tune later):
- sample every 100ms (t0 grid)
- slope windows W: 2000ms, 5000ms
- horizons x: 5000ms, 10000ms
- slope formula: linear regression slope of ln(mid) vs time

Usage:
  python3 run_slope_research.py --input parsed_BTCUSDT.csv
  python3 run_slope_research.py --input ./data --glob "*.csv"
"""

import argparse
import os
import glob
import numpy as np
import pandas as pd

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" not in df.columns:
        raise ValueError("Missing column: timestamp")
    # Accept either (price1, price2) or (bid, ask)
    if {"price1","price2"}.issubset(df.columns):
        p1, p2 = "price1", "price2"
    elif {"bid","ask"}.issubset(df.columns):
        p1, p2 = "bid", "ask"
    else:
        raise ValueError("Need either columns price1+price2 or bid+ask")

    df = df.sort_values("timestamp").reset_index(drop=True)
    df["t_ms"] = df["timestamp"].astype("int64")
    df["mid"] = (df[p1].astype(float) + df[p2].astype(float)) / 2.0
    df = df.dropna(subset=["t_ms","mid"])
    return df[["t_ms","mid"]]

def slope_lr_bps_per_s(df: pd.DataFrame, t0_grid: np.ndarray, window_ms: int, min_points: int = 10) -> np.ndarray:
    times = df["t_ms"].to_numpy()
    lnp = np.log(df["mid"].to_numpy())
    out = []
    for t in t0_grid:
        lo = t - window_ms
        idx = np.where((times >= lo) & (times <= t))[0]
        if idx.size < min_points:
            out.append(np.nan)
            continue
        x = times[idx].astype(np.float64)
        y = lnp[idx].astype(np.float64)
        x_mean = x.mean()
        y_mean = y.mean()
        denom = ((x - x_mean) ** 2).sum()
        if denom == 0:
            out.append(np.nan)
            continue
        beta = ((x - x_mean) * (y - y_mean)).sum() / denom  # per ms
        out.append(beta * 1000.0 * 10000.0)  # bps/sec
    return np.array(out, dtype=float)

def future_return(df: pd.DataFrame, t0: pd.DataFrame, x_ms: int) -> np.ndarray:
    fut = t0[["t0_ms","mid0"]].copy()
    fut["t1_ms"] = fut["t0_ms"] + x_ms
    t1map = df.rename(columns={"t_ms":"t1_ms","mid":"mid1"})
    fut = pd.merge_asof(
        fut.sort_values("t1_ms"),
        t1map.sort_values("t1_ms"),
        on="t1_ms",
        direction="backward"
    )
    return np.log(fut["mid1"] / fut["mid0"]).to_numpy()

def decile_summary(out: pd.DataFrame, col: str) -> pd.DataFrame:
    s = out[col].dropna()
    if s.empty:
        return pd.DataFrame()
    q = pd.qcut(s, 10, labels=False, duplicates="drop") + 1
    tmp = out.loc[s.index].copy()
    tmp[f"{col}_decile"] = q.values
    return tmp.groupby(f"{col}_decile", as_index=False).agg(
        n=("mid0","size"),
        avg_slope=(col,"mean"),
        avg_ret_5s=("ret_5s","mean"),
        avg_ret_10s=("ret_10s","mean"),
        pct_pos_5s=("ret_5s", lambda x: (x>0).mean()),
        pct_pos_10s=("ret_10s", lambda x: (x>0).mean()),
    )

def process_one_file(in_path: str, out_dir: str, step_ms: int, slope_windows_ms: list[int], horizons_ms: list[int], min_points: int):
    raw = pd.read_csv(in_path)
    df = normalize_df(raw)

    t0_grid = np.arange(df["t_ms"].min(), df["t_ms"].max() + 1, step_ms, dtype=np.int64)
    t0 = pd.DataFrame({"t0_ms": t0_grid})

    # map mid at t0 (last-known quote)
    base = df.rename(columns={"t_ms":"t0_ms","mid":"mid0"})
    t0 = pd.merge_asof(t0.sort_values("t0_ms"), base.sort_values("t0_ms"), on="t0_ms", direction="backward")

    # slopes
    for w in slope_windows_ms:
        t0[f"slope_{w}ms_bps_s"] = slope_lr_bps_per_s(df, t0_grid, w, min_points=min_points)

    # future returns
    for x in horizons_ms:
        t0[f"ret_{x}ms"] = future_return(df, t0, x)

    # friendly columns for default horizons
    if 5000 in horizons_ms:
        t0["ret_5s"] = t0["ret_5000ms"]
    if 10000 in horizons_ms:
        t0["ret_10s"] = t0["ret_10000ms"]

    out = t0.dropna(subset=["mid0"]).reset_index(drop=True)

    base_name = os.path.splitext(os.path.basename(in_path))[0]
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, f"features_{base_name}.csv")
    out_xlsx = os.path.join(out_dir, f"mvp_{base_name}.xlsx")
    out.to_csv(out_csv, index=False)

    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        out.to_excel(writer, sheet_name="features", index=False)
        # summaries for each slope
        for w in slope_windows_ms:
            col = f"slope_{w}ms_bps_s"
            summ = decile_summary(out, col)
            summ.to_excel(writer, sheet_name=f"deciles_{w}ms", index=False)

    return out_csv, out_xlsx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV file path OR folder path")
    ap.add_argument("--glob", default="*.csv", help="If input is a folder, which files to include")
    ap.add_argument("--out", default="./out_research", help="Output folder")
    ap.add_argument("--step-ms", type=int, default=100, help="Sampling step for t0 grid")
    ap.add_argument("--slope-windows-ms", default="2000,5000", help="Comma list (e.g. 500,2000,5000)")
    ap.add_argument("--horizons-ms", default="5000,10000", help="Comma list (e.g. 500,2000,5000,10000)")
    ap.add_argument("--min-points", type=int, default=10, help="Min points required inside a slope window")
    ap.add_argument("--combine", action="store_true", help="Write a master CSV combining all features")
    args = ap.parse_args()

    slope_windows_ms = [int(x.strip()) for x in args.slope_windows_ms.split(",") if x.strip()]
    horizons_ms = [int(x.strip()) for x in args.horizons_ms.split(",") if x.strip()]

    # gather files
    files = []
    if os.path.isdir(args.input):
        files = sorted(glob.glob(os.path.join(args.input, args.glob)))
    else:
        files = [args.input]

    all_out = []
    for f in files:
        out_csv, out_xlsx = process_one_file(
            f, args.out, args.step_ms, slope_windows_ms, horizons_ms, args.min_points
        )
        print(f"[OK] {f} -> {out_csv} , {out_xlsx}")
        if args.combine:
            tmp = pd.read_csv(out_csv)
            tmp["source_file"] = os.path.basename(f)
            all_out.append(tmp)

    if args.combine and all_out:
        master = pd.concat(all_out, ignore_index=True)
        master_path = os.path.join(args.out, "MASTER_features_all_files.csv")
        master.to_csv(master_path, index=False)
        print(f"[OK] Master written: {master_path}")

if __name__ == "__main__":
    main()
