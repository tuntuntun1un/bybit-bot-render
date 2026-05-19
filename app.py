import requests
import time
import hashlib
import hmac
from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET_KEY = "my_secret_2025"

API_KEY = "N3wh1oRNeHPVQJF6LWcKsW28JjU9y8qWb0vCwXTmUTrcnCWSE2iiYxBTEks8xh"
API_SECRET = "11k0dgnvaHa27fAi8zZfger7tCh13ES0ckj6TTVHZtmFqfR2emi2V6LM36T1GzuNa"

BASE_URL = "https://testnet.binance.vision"

def test_connection():
    """Проверка подключения к Binance Testnet (запрос баланса)"""
    timestamp = int(time.time() * 1000)
    params = {
        "timestamp": timestamp,
        "recvWindow": 5000
    }
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(bytes(API_SECRET, 'utf-8'), bytes(query_string, 'utf-8'), hashlib.sha256).hexdigest()
    headers = {'X-MBX-APIKEY': API_KEY}
    url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    print("🔥 Webhook вызван!")
    try:
        data = request.get_json()
        print(f"📡 Данные: {data}")
        
        if data.get('secret') != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        
        # Тест подключения
        balance = test_connection()
        print(f"✅ Ответ Binance (баланс): {balance}")
        
        if 'balances' in balance:
            return jsonify({"status": "ok", "message": "API key works!"}), 200
        else:
            return jsonify({"error": balance}), 500
            
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 ТЕСТОВЫЙ БОТ ЗАПУЩЕН!")
    app.run(host='0.0.0.0', port=5002)
