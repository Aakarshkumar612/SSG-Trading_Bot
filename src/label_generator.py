# src/label_generator.py — Labels historical data for training

import pandas as pd
from config import TARGET_POINTS, STOPLOSS_POINTS, TIME_LIMIT_SEC, LABEL_BUY, LABEL_SELL, LABEL_NONE

def generate_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each row, look ahead 5 seconds worth of ticks.
    Label it: BUY_FAST, SELL_FAST, or NO_MOVE
    """
    labels = []

    for i in range(len(df)):
        current_price = df.iloc[i]["ltp"]
        buy_target    = current_price + TARGET_POINTS     # e.g. ₹151
        sell_target   = current_price - STOPLOSS_POINTS   # e.g. ₹149

        label = LABEL_NONE  # default

        # Look at future rows (next 5 seconds)
        future = df.iloc[i+1 : i+50]  # approx 50 ticks = 5 seconds

        for _, future_row in future.iterrows():
            future_price = future_row["ltp"]

            if future_price >= buy_target:
                label = LABEL_BUY    # price hit +₹1 first
                break
            elif future_price <= sell_target:
                label = LABEL_SELL   # price hit -₹1 first
                break

        labels.append(label)

    df["label"] = labels
    return df