import pandas as pd
import matplotlib.pyplot as plt

FILE = "BTCUSDT_20260212.txt"  # change to your data file

# reads whitespace-separated file: timestamp bid ask
df = pd.read_csv(FILE, sep=r"\s+", names=["ts", "bid", "ask"], engine="python")

# convert timestamp (ms) to datetime
df["time"] = pd.to_datetime(df["ts"], unit="ms")

# mid = average of bid and ask
df["mid"] = (df["bid"] + df["ask"]) / 2

# downsample if too many points (every 100 rows)
df_plot = df.iloc[::100].copy()

plt.figure()
plt.plot(df_plot["time"], df_plot["mid"])
plt.xlabel("time")
plt.ylabel("mid (avg of bid/ask)")
plt.title("mid price over time")
plt.show()
