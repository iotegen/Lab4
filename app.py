from flask import Flask, request, jsonify
import json
import traceback
from itsdangerous import URLSafeSerializer

app = Flask(__name__)

# Загружаем локальный конфиг (в demo он содержит "секреты", но он в .gitignore)
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

@app.route("/debug")
def debug():
    try:
        raise Exception(f"Something went wrong: DB host = {config['db']['host']}")
    except Exception as e:
        return jsonify({"message": str(e), "stack": traceback.format_exc()}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    if data.get("username") == "admin" and data.get("password") == "AdminPass123!":
        return jsonify({"ok": True, "token": "hardcoded-python-token"})
    return jsonify({"ok": False}), 401

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.get_json() or {}
    s = URLSafeSerializer("hardcoded-secret-key")
    try:
        obj = s.loads(data.get("data",""))
        return jsonify({"ok": True, "obj": obj})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
