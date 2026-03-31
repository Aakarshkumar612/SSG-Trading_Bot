# app.py — FastAPI web server for SSG Trading Bot Dashboard

import os
import json
import threading
import time
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from main import main as run_trading_bot

app = FastAPI(title="SSG Trading Bot", version="1.0.0")

# ── CORS Middleware ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve Dashboard ────────────────────────────────────────────
@app.get("/")
def dashboard():
    """Serve the main HTML dashboard."""
    return FileResponse("index.html", media_type="text/html")

@app.get("/live_data.json")
def live_data():
    """Serve the live trading data as JSON."""
    try:
        if os.path.exists("live_data.json"):
            with open("live_data.json", "r") as f:
                data = json.load(f)
            return data
        else:
            # Return default data if bot hasn't started yet
            return {
                "ltp": 199.50,
                "prediction": "WAITING...",
                "active_trade": False,
                "trade_type": "",
                "entry_price": 0,
                "total_pnl": 0,
                "trade_count": 0,
                "timestamp": time.strftime("%H:%M:%S")
            }
    except Exception as e:
        print(f"❌ Error reading live_data.json: {e}")
        return {"error": "Data not available yet"}, 500

# ── Health Check ───────────────────────────────────────────────
@app.get("/health")
def health():
    """Health check endpoint for Render."""
    return {"status": "ok"}

# ── API Status ─────────────────────────────────────────────────
@app.get("/api/status")
def api_status():
    """Get trading bot status."""
    try:
        if os.path.exists("live_data.json"):
            with open("live_data.json", "r") as f:
                data = json.load(f)
            return {
                "running": True,
                "data": data
            }
        else:
            return {
                "running": False,
                "message": "Bot not started yet"
            }
    except Exception as e:
        return {"error": str(e)}, 500

# ── Static Files (CSS, JS, etc.) ────────────────────────────────
@app.get("/{file_path:path}")
def serve_static(file_path: str):
    """Serve static files."""
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}, 404

# ── Start Trading Bot in Background ────────────────────────────
def start_bot():
    """Run the trading bot in a separate thread."""
    print("🤖 Trading Bot Thread Started")
    try:
        run_trading_bot()
    except Exception as e:
        print(f"❌ Trading Bot Error: {e}")

# ── Startup Event ──────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Start trading bot on server startup."""
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    print("✅ FastAPI Server Started")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
