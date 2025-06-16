from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_live_price_yahoo(pair_symbol):
    try:
        symbol = pair_symbol.upper().replace("/", "") + "=X"
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": f"Yahoo returned status {response.status_code}"}

        data = response.json()

        # Check if the chart exists
        if "chart" not in data or "result" not in data["chart"] or data["chart"]["result"] is None:
            return {"error": "Invalid or empty result from Yahoo"}

        result = data['chart']['result'][0]
        meta = result['meta']
        current_price = meta.get('regularMarketPrice')

        if current_price is None:
            return {"error": "Price not found in Yahoo response"}

        return {"pair": pair_symbol, "price": current_price}

    except Exception as e:
        return {"error": str(e)}

@app.route("/price")
def get_price():
    pair = request.args.get("pair", "EUR/USD")
    result = get_live_price_yahoo(pair)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
