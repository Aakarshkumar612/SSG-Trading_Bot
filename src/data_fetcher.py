# src/data_fetcher.py — Realistic tick simulator

import time
import random

# ── Persistent price state (simulates a real stock) ──────────────
_current_price = 200.0
_current_volume = 10000

def get_live_data(symbol: str) -> dict:
    global _current_price, _current_volume

    # Small realistic price move like a real stock
    change = random.choice([-0.5, -0.25, 0.0, 0.25, 0.5])
    _current_price = round(_current_price + change, 2)
    _current_price = max(100, min(500, _current_price))  # keep in range

    # Realistic bid/ask around current price
    bid_price = round(_current_price - 0.10, 2)
    ask_price = round(_current_price + 0.10, 2)

    # Volume grows over time
    _current_volume += random.randint(10, 200)

    return {
        "symbol"    : symbol,
        "ltp"       : _current_price,
        "bid_price" : bid_price,
        "ask_price" : ask_price,
        "bid_qty"   : random.randint(200, 3000),
        "ask_qty"   : random.randint(200, 3000),
        "volume"    : _current_volume,
        "timestamp" : time.time()
    }