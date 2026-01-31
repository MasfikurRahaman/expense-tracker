from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

expenses = []

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/api/expense", methods=["GET", "POST"])
def expense():
    if request.method == "POST":
        data = request.get_json()
        expense = {
            "id": str(uuid.uuid4()),
            "user": data.get("user"),
            "title": data.get("title"),
            "amount": data.get("amount")
        }
        expenses.append(expense)
        return jsonify(expense), 201

    return jsonify(expenses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

