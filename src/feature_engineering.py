# src/feature_engineering.py — Converts market data into AI features

def calculate_features(current: dict, previous: dict) -> dict:
    """
    Input : current tick data + previous tick data
    Output: feature dictionary for ML model
    """

    # ── Feature 1: Market Depth Ratio (MDR) ──────────────────────
    # MDR > 1 → more buyers → price likely goes UP
    # MDR < 1 → more sellers → price likely goes DOWN
    bid_qty = current["bid_qty"]
    ask_qty = current["ask_qty"]
    mdr = bid_qty / ask_qty if ask_qty != 0 else 1.0

    # ── Feature 2: Volume Delta ───────────────────────────────────
    # How fast is volume increasing? Fast = strong movement
    prev_volume = previous.get("volume", current["volume"])
    volume_delta = current["volume"] - prev_volume

    # ── Feature 3: Spread ─────────────────────────────────────────
    # Small spread = active market, Large spread = weak movement
    spread = current["ask_price"] - current["bid_price"]

    # ── Feature 4: Price Trend ────────────────────────────────────
    # +1 = price rising, -1 = price falling, 0 = no change
    prev_ltp = previous.get("ltp", current["ltp"])
    if current["ltp"] > prev_ltp:
        trend = 1
    elif current["ltp"] < prev_ltp:
        trend = -1
    else:
        trend = 0

    # ── Feature 5: Aggression (who is attacking?) ─────────────────
    # Buyers attacking  → ltp == ask_price → value = +1
    # Sellers attacking → ltp == bid_price → value = -1
    if current["ltp"] == current["ask_price"]:
        aggression = 1      # buyers aggressive
    elif current["ltp"] == current["bid_price"]:
        aggression = -1     # sellers aggressive
    else:
        aggression = 0

    # ── Feature 6: Trade Speed ────────────────────────────────────
    # How fast is price changing per second?
    time_diff = current["timestamp"] - previous.get("timestamp", current["timestamp"])
    price_diff = abs(current["ltp"] - prev_ltp)
    trade_speed = price_diff / time_diff if time_diff > 0 else 0

    return {
        "mdr"          : round(mdr, 4),
        "volume_delta" : volume_delta,
        "spread"       : round(spread, 4),
        "trend"        : trend,
        "aggression"   : aggression,
        "trade_speed"  : round(trade_speed, 4)
    }