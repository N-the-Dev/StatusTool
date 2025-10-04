from flask import Flask, jsonify
import json, os

app = Flask(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Remote Tool Manager API is running.",
        "routes": ["/status"]
    })

@app.route("/status", methods=["GET"])
def status():
    config = load_config()
    return jsonify(config)
