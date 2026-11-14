import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-demo-change-this-key")
employees = [
    {"id": 1, "name": "Arun", "department": "Cloud", "status": "Present"},
    {"id": 2, "name": "Priya", "department": "HR", "status": "Present"},
    {"id": 3, "name": "Kumar", "department": "DevOps", "status": "On Leave"},
]

@app.route("/")
def index():
    return render_template("index.html", employees=employees,
                           app_env=os.getenv("APP_ENV", "development"),
                           pod_name=os.getenv("HOSTNAME", "local"))

@app.route("/check-in", methods=["POST"])
def check_in():
    name = request.form.get("name", "").strip()
    if name:
        employees.append({"id": max((e["id"] for e in employees), default=0) + 1,
                          "name": name, "department": "New Joiner", "status": "Present"})
        flash(f"{name} checked in successfully.")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/ready")
def ready():
    return {"status": "ready"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
