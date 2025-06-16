from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "2a030314530e42eea9fe5bdf21f53390"

def get_live_price_twelvedata(pair_symbol):
    try:
        symbol = pair_symbol.upper()  # Keep slash for TwelveData
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": f"TwelveData returned status {response.status_code}"}

        data = response.json()

        if "price" in data:
            return {"pair": pair_symbol, "price": float(data["price"])}
        else:
            return {"error": data.get("message", "Unknown error")}
    except Exception as e:
        return {"error": str(e)}

@app.route("/price")
def get_price():
    pair = request.args.get("pair", "EUR/USD")
    result = get_live_price_twelvedata(pair)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
