import requests
import time
import hashlib
import hmac
import json
from flask import Flask, request, jsonify

# --- ОПРЕДЕЛЕНИЕ IP СЕРВЕРА (без лишних библиотек) ---
try:
    ip_response = requests.get('https://api.ipify.org', timeout=5)
    server_ip = ip_response.text.strip()
    print(f"🌍 Публичный IP сервера: {server_ip}")
except Exception as e:
    print(f"⚠️ Не удалось определить IP: {e}")
# ---------------------------------------------------

app = Flask(__name__)

SECRET_KEY = "my_secret_2025"
SYMBOL = "XRPUSDT"
BASE_URL = "https://api-testnet.bybit.com"

API_KEY = "OfFL3zuIKkZBMVKcK"
API_SECRET = "n6AqlvTeplWOA2OMPXy59AOUoqP6kGld2MAo"
PROXY_URL = "http://user410083:37zj0n@192.124.191.79:7824"

proxies = {'http': PROXY_URL, 'https': PROXY_URL}

def place_order(side, qty):
    timestamp = int(time.time() * 1000)
    order_payload = {
        "category": "linear",
        "symbol": SYMBOL,
        "side": side,
        "orderType": "Market",
        "qty": qty,
        "timeInForce": "GTC",
    }
    payload_str = json.dumps(order_payload)
    recv_window = "5000"
    signature_payload = f"{timestamp}{API_KEY}{recv_window}{payload_str}"
    signature = hmac.new(bytes(API_SECRET, 'utf-8'), bytes(signature_payload, 'utf-8'), hashlib.sha256).hexdigest()
    headers = {
        'X-BAPI-API-KEY': API_KEY,
        'X-BAPI-TIMESTAMP': str(timestamp),
        'X-BAPI-SIGN': signature,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{BASE_URL}/v5/order/create", headers=headers, data=payload_str, proxies=proxies)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    print("🔥 Webhook вызван!")
    try:
        data = request.get_json()
        print(f"📡 Данные: {data}")
        if data.get('secret') != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        signal = data.get('signal')
        if signal not in ['buy', 'sell']:
            return jsonify({"error": "Invalid signal"}), 400
        side = "Buy" if signal == 'buy' else "Sell"
        qty = "10"
        print(f"🚀 Отправка ордера {side} {qty} XRP через прокси")
        result = place_order(side, qty)
        print(f"✅ Ответ Bybit: {result}")
        if result.get('retCode') == 0:
            return jsonify({"status": "ok", "orderId": result['result']['orderId']}), 200
        else:
            return jsonify({"error": result}), 500
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
