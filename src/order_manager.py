# src/order_manager.py — Trade entry/exit manager

import time
from config import TARGET_POINTS, STOPLOSS_POINTS, TIME_LIMIT_SEC

class OrderManager:
    def __init__(self):
        self.active_trade      = None
        self.entry_price       = None
        self.trade_type        = None
        self.entry_time        = None
        self.total_pnl         = 0.0
        self.trade_count       = 0
        self.last_trade_type   = None    # ← new
        self.last_entry_price  = None    # ← new

    def enter_trade(self, trade_type: str, price: float):
        self.active_trade     = True
        self.trade_type       = trade_type
        self.entry_price      = price
        self.entry_time       = time.time()
        self.last_trade_type  = trade_type
        self.last_entry_price = price
        print(f"\n✅ {trade_type} entered at ₹{price}")

    def check_exit(self, current_price: float):
        if not self.active_trade:
            return

        pnl    = 0
        reason = None
        elapsed = time.time() - self.entry_time

        if self.trade_type == "BUY":
            if current_price >= self.entry_price + TARGET_POINTS:
                pnl    = TARGET_POINTS
                reason = "TARGET HIT 🎯"
            elif current_price <= self.entry_price - STOPLOSS_POINTS:
                pnl    = -STOPLOSS_POINTS
                reason = "STOPLOSS HIT 🛑"

        elif self.trade_type == "SELL":
            if current_price <= self.entry_price - TARGET_POINTS:
                pnl    = TARGET_POINTS
                reason = "TARGET HIT 🎯"
            elif current_price >= self.entry_price + STOPLOSS_POINTS:
                pnl    = -STOPLOSS_POINTS
                reason = "STOPLOSS HIT 🛑"

        if reason is None and elapsed > TIME_LIMIT_SEC:
            pnl    = 0
            reason = "TIME LIMIT ⏱️"

        if reason:
            self.close_trade(pnl, reason)

    def close_trade(self, pnl: float, reason: str):
        self.total_pnl   += pnl
        self.trade_count += 1
        print(f"📤 Trade closed | Reason: {reason} | P&L: ₹{pnl} | Total P&L: ₹{self.total_pnl}")
        self.active_trade = None
        self.entry_price  = None
        self.trade_type   = None
        self.entry_time   = None