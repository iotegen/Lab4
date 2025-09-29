# app.py (fixed)
from flask import Flask, request, jsonify
import json
import logging
import os

app = Flask(__name__)

# load example config (no secrets)
with open("config/config.example.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

# use env vars for secrets (local: set these in your shell; never commit .env)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "replace_with_secure_password")

# logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

def handle_error(err):
    logger.exception(err)
    return jsonify({"message": "Internal server error"}), 500

@app.route("/debug")
def debug():
    try:
        # demo endpoint — but we don't reveal internals
        raise Exception("Intentional demo error")
    except Exception as e:
        return handle_error(e)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    if data.get("username") == ADMIN_USERNAME and data.get("password") == ADMIN_PASSWORD:
        # TODO: generate real JWT in production
        return jsonify({"ok": True, "token": "TODO:generate-jwt"}), 200
    return jsonify({"ok": False}), 401

@app.route("/deserialize", methods=["POST"])
def deserialize():
    # safe handling: accept JSON and validate expected structure (no unserialize)
    payload = request.get_json() or {}
    name = payload.get("name")
    if not name or not isinstance(name, str):
        return jsonify({"ok": False, "error": "Invalid payload: name required"}), 400
    return jsonify({"ok": True, "data": {"name": name}}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=(os.getenv("FLASK_ENV") != "production"))
