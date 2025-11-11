from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import math

app = Flask(__name__, static_folder="frontend/build")
CORS(app)

# ------------------------------
# Global cache
# ------------------------------
STOCK_DATA_CACHE = {}  # {ticker: {...}}
CACHE_TIMESTAMP = None

# ------------------------------
# Example API endpoint
# ------------------------------
@app.route("/api/status")
def status():
    age = (datetime.now() - CACHE_TIMESTAMP).seconds if CACHE_TIMESTAMP else 0
    return jsonify({
        "ready": bool(STOCK_DATA_CACHE),
        "stock_count": len(STOCK_DATA_CACHE),
        "cache_age_sec": age
    })

@app.route("/api/query", methods=["POST"])
def query():
    data = request.json
    query_text = data.get("query", "").lower()
    # Example: just return all cached tickers for now
    results = []
    for ticker, info in STOCK_DATA_CACHE.items():
        results.append({
            "ticker": ticker,
            "current_price": info.get("current_price", 0),
            "current_dcf": info.get("current_dcf", 0)
        })
    return jsonify({"stocks": results})

# ------------------------------
# Serve React frontend
# ------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# ------------------------------
# Example initialization function
# ------------------------------
def initialize_data():
    global STOCK_DATA_CACHE, CACHE_TIMESTAMP
    tickers = ["AAPL", "MSFT", "GOOG"]  # Example; replace with real logic
    for t in tickers:
        STOCK_DATA_CACHE[t] = {
            "current_price": yf.Ticker(t).info.get("regularMarketPrice", 0),
            "current_dcf": 100  # Example placeholder
        }
    CACHE_TIMESTAMP = datetime.now()
    print(f"Initialized {len(STOCK_DATA_CACHE)} stocks")

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    from threading import Thread
    Thread(target=initialize_data, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
