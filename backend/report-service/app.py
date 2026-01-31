from flask import Flask, jsonify
import requests

app = Flask(__name__)

EXPENSE_SERVICE = "http://expense-service:5000"

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/api/report/summary")
def summary():
    expenses = requests.get(f"{EXPENSE_SERVICE}/api/expense").json()
    total = sum(e["amount"] for e in expenses)
    return jsonify({
        "count": len(expenses),
        "total_amount": total
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

