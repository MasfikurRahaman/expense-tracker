from flask import Flask, render_template, request, redirect, url_for, session
import requests
import logging

app = Flask(__name__)
app.secret_key = "microservices-devops-secret"

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ---------------- CONFIG ----------------
USERS = ["admin1", "admin2", "admin3"]

# Backend service URLs (K8s service names)
EXPENSE_SERVICE = "http://expense-service:5000"

# ---------------- ROUTES ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and password == username:
            session["user"] = username
            logging.info(f"User logged in: {username}")
            return redirect(url_for("home"))
        else:
            logging.warning(f"Failed login attempt for user: {username}")
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])


@app.route("/expense")
def expense():
    if "user" not in session:
        return redirect(url_for("login"))

    expenses = []
    error = None

    try:
        response = requests.get(f"{EXPENSE_SERVICE}/api/expense", timeout=2)
        if response.status_code == 200:
            expenses = response.json()
        else:
            error = "Expense service returned error"
            logging.error("Expense service error response")
    except Exception as e:
        error = "Expense service not reachable"
        logging.error(f"Expense service connection failed: {e}")

    return render_template(
        "expense.html",
        expenses=expenses,
        error=error
    )


@app.route("/logout")
def logout():
    user = session.pop("user", None)
    if user:
        logging.info(f"User logged out: {user}")
    return redirect(url_for("login"))


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

