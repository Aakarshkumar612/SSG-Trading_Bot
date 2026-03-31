# main.py — Main trading loop with trade logging

import time
import datetime
import csv
import os
from config import LTP_MIN, LTP_MAX, LABEL_BUY, LABEL_SELL
from src.data_fetcher        import get_live_data
from src.feature_engineering import calculate_features
from src.predictor           import Predictor
from src.order_manager       import OrderManager

SYMBOL     = "RELIANCE"
MAX_TRADES = 50

def main():
    print("🚀 SSG Trading Bot Starting...\n")

    predictor     = Predictor()
    order_manager = OrderManager()
    previous_tick = {}
    trade_log     = []   # ← stores every trade for the report

    while True:
        try:
            tick = get_live_data(SYMBOL)
            ltp  = tick["ltp"]
            print(f"📈 LTP: ₹{ltp}", end=" | ")

            if not (LTP_MIN <= ltp <= LTP_MAX):
                print("⛔ Out of range, skipping")
                time.sleep(0.1)
                continue

            features    = calculate_features(tick, previous_tick)
            before_pnl  = order_manager.total_pnl

            order_manager.check_exit(ltp)

            # ── Log completed trades ──────────────────────────────
            after_pnl = order_manager.total_pnl
            if after_pnl != before_pnl:
                pnl   = after_pnl - before_pnl
                trade_log.append({
                    "trade_no"   : order_manager.trade_count,
                    "type"       : order_manager.last_trade_type,
                    "entry"      : order_manager.last_entry_price,
                    "exit"       : ltp,
                    "pnl"        : pnl,
                    "total_pnl"  : after_pnl,
                    "result"     : "WIN" if pnl > 0 else "LOSS",
                    "time"       : datetime.datetime.now().strftime("%H:%M:%S")
                })

            if not order_manager.active_trade:
                prediction = predictor.predict(features)
                print(f"🤖 Prediction: {prediction}")
                if prediction == LABEL_BUY:
                    order_manager.enter_trade("BUY", ltp)
                elif prediction == LABEL_SELL:
                    order_manager.enter_trade("SELL", ltp)
                else:
                    print("⏸️  No trade")

            if order_manager.trade_count >= MAX_TRADES:
                print(f"\n✅ Reached {MAX_TRADES} trades. Stopping.")
                print(f"📊 Final P&L   : ₹{order_manager.total_pnl}")
                print(f"📊 Total Trades: {order_manager.trade_count}")
                break

            previous_tick = tick

            # ── Write live data for dashboard ────────────────────────────
            import json

            live = {
                "ltp"         : tick["ltp"],
                "prediction"  : prediction if not order_manager.active_trade else "IN_TRADE",
                "active_trade": order_manager.active_trade or False,
                "trade_type"  : order_manager.trade_type or "",
                "entry_price" : order_manager.entry_price or 0,
                "total_pnl"   : order_manager.total_pnl,
                "trade_count" : order_manager.trade_count,
                "timestamp"   : time.strftime("%H:%M:%S")
            }

            with open("live_data.json", "w") as f:
                json.dump(live, f)

            time.sleep(0.1)

        except KeyboardInterrupt:
            print(f"\n🛑 Bot stopped manually")
            print(f"📊 Final P&L   : ₹{order_manager.total_pnl}")
            print(f"📊 Total Trades: {order_manager.trade_count}")
            break

    # ── Save trade log to CSV ─────────────────────────────────────
    if trade_log:
        os.makedirs("reports", exist_ok=True)
        csv_path = "reports/trade_log.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=trade_log[0].keys())
            writer.writeheader()
            writer.writerows(trade_log)
        print(f"💾 Trade log saved → {csv_path}")

        # ── Generate PDF report ───────────────────────────────────
        from generate_report import generate_pdf_report
        generate_pdf_report(trade_log, order_manager)

if __name__ == "__main__":
    main()