from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = ["admin1", "admin2", "admin3"]

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/api/user/validate", methods=["POST"])
def validate_user():
    data = request.get_json()
    username = data.get("username")

    if username in USERS:
        return jsonify({"valid": True, "user": username})
    return jsonify({"valid": False}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

