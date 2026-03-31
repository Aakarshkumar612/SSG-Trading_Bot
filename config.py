# config.py — All settings for the trading bot

# ── Price Filter ──────────────────────────────
LTP_MIN = 100       # Only trade stocks above ₹100
LTP_MAX = 1000      # Only trade stocks below ₹1000

# ── Trade Rules ───────────────────────────────
TARGET_POINTS   = 1.0    # Take profit at +₹1
STOPLOSS_POINTS = 1.0    # Stop loss at -₹1
TIME_LIMIT_SEC  = 5      # Exit trade after 5 seconds if no movement

# ── Model Labels ──────────────────────────────
LABEL_BUY    = "BUY_FAST"
LABEL_SELL   = "SELL_FAST"
LABEL_NONE   = "NO_MOVE"

# ── File Paths ────────────────────────────────
DATA_PATH  = "data/market_data.csv"
MODEL_PATH = "models/trading_model.pkl"

# ── Broker API (replace with real values) ─────
API_KEY    = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"