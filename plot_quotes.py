import pandas as pd
import matplotlib.pyplot as plt

FILE = "BTCUSDT_20260212.txt"  # שנה לשם הקובץ שלך

# קורא קובץ שמופרד ברווחים: timestamp bid ask
df = pd.read_csv(FILE, sep=r"\s+", names=["ts", "bid", "ask"], engine="python")

# הופך timestamp לזמן אמיתי (ms)
df["time"] = pd.to_datetime(df["ts"], unit="ms")

# ממוצע bid/ask = mid
df["mid"] = (df["bid"] + df["ask"]) / 2

# אם יש יותר מדי נקודות, מדללים (כל 100 שורות למשל)
df_plot = df.iloc[::100].copy()

plt.figure()
plt.plot(df_plot["time"], df_plot["mid"])
plt.xlabel("time")
plt.ylabel("mid (avg of bid/ask)")
plt.title("BTCUSDT mid price")
plt.show()
