import requests
import time
import hashlib
import hmac
import json
from flask import Flask, request, jsonify

# --- КОД ДЛЯ ОПРЕДЕЛЕНИЯ IP СЕРВЕРА ---
try:
    response = requests.get('https://api.ipify.org', timeout=5)
    server_ip = response.text.strip()
    print(f"🌍 Публичный IP-адрес этого сервера: {server_ip}")
except Exception as e:
    print(f"⚠️ Не удалось определить IP: {e}")
# -------------------------------------

app = Flask(__name__)

# ... (весь остальной код бота без изменений) ...
