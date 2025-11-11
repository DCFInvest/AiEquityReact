from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample stock data (replace with your full DCF logic)
STOCK_DATA = {
    "AAPL": {"current_price": 175, "current_dcf": 200, "sector": "Technology"},
    "MSFT": {"current_price": 320, "current_dcf": 350, "sector": "Technology"},
}

@app.route("/api/query", methods=["POST"])
def query_stocks():
    data = request.json
    query = data.get("query", "").lower()
    result = []
    for ticker, info in STOCK_DATA.items():
        if query in ticker.lower() or query in info["sector"].lower():
            result.append({"ticker": ticker, **info})
    return jsonify(result)

@app.route("/api/status")
def status():
    return jsonify({"status": "running", "stocks": len(STOCK_DATA)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
