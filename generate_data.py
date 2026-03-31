# generate_data.py — Realistic market simulation

import pandas as pd
import numpy as np
import os

np.random.seed(42)
rows = 5000

# ── Simulate realistic tick-by-tick price movement ──────────────
prices = [200.0]  # start at ₹200
for _ in range(rows - 1):
    change = np.random.choice(
        [-0.5, -0.25, 0, 0.25, 0.5],       # small realistic moves
        p=[0.2, 0.2, 0.2, 0.2, 0.2]
    )
    new_price = round(prices[-1] + change, 2)
    new_price = max(100, min(500, new_price))  # keep in range
    prices.append(new_price)

prices = np.array(prices)

# ── Simulate realistic bid/ask/volume around price ──────────────
df = pd.DataFrame({
    "ltp"          : prices,
    "bid_price"    : prices - 0.10,
    "ask_price"    : prices + 0.10,
    "bid_qty"      : np.random.randint(200, 3000, rows),
    "ask_qty"      : np.random.randint(200, 3000, rows),
    "volume"       : np.cumsum(np.random.randint(10, 200, rows)),
    "timestamp"    : np.cumsum(np.random.uniform(0.05, 0.15, rows))
})

# ── Calculate features ───────────────────────────────────────────
df["mdr"]          = df["bid_qty"] / df["ask_qty"]
df["volume_delta"] = df["volume"].diff().fillna(0)
df["spread"]       = df["ask_price"] - df["bid_price"]
df["trend"]        = np.sign(df["ltp"].diff().fillna(0))
df["aggression"]   = 0
df["trade_speed"]  = df["ltp"].diff().abs().fillna(0) / df["timestamp"].diff().fillna(1)

# ── Generate realistic labels ─────────────────────────────────
labels = []
for i in range(len(df)):
    current = df.iloc[i]["ltp"]
    buy_target  = current + 1.0
    sell_target = current - 1.0
    label = "NO_MOVE"

    future = df.iloc[i+1 : i+30]   # look 30 ticks ahead
    for _, row in future.iterrows():
        if row["ltp"] >= buy_target:
            label = "BUY_FAST"
            break
        elif row["ltp"] <= sell_target:
            label = "SELL_FAST"
            break

    labels.append(label)

df["label"] = labels

os.makedirs("data", exist_ok=True)
df.to_csv("data/market_data.csv", index=False)

# ── Print summary ────────────────────────────────────────────────
print(f"✅ Generated {rows} rows → data/market_data.csv")
print(f"📊 Label distribution:")
print(df["label"].value_counts())
print(f"📈 Price range: ₹{df['ltp'].min()} - ₹{df['ltp'].max()}")