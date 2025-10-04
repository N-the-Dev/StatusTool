from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Remote Tool Manager API đang hoạt động",
        "routes": ["/status", "/update"]
    })

@app.route("/status", methods=["GET"])
def status():
    config = load_config()
    return jsonify(config)

@app.route("/update", methods=["POST"])
def update():
    """Cập nhật cấu hình (chỉ nên dùng nếu có bảo mật hoặc deploy riêng)"""
    data = request.json
    config = load_config()
    for key in ["latest_version", "status", "message"]:
        if key in data:
            config[key] = data[key]

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    return jsonify({"success": True, "new_config": config})

# Đoạn này giúp Flask chạy được trên Vercel (cần export app)
def handler(event, context):
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
