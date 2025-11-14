from flask import Flask, jsonify, send_from_directory
import pathlib

app = Flask(__name__, static_folder="static", static_url_path="")

TASKS = [
    {"title": "Audit inbound leads", "category": "sales", "icon": "??", "status": "pending", "note": "Needs PR review"},
    {"title": "Refactor login widget with new theme", "category": "engineer", "icon": "??", "status": "in-progress", "note": "Edge-case around spacing"},
    {"title": "Ship onboarding copy refresh for internal docs", "category": "design", "icon": "??", "status": "blocked", "note": "Waiting on legal"},
    {"title": "Monitor server-latency spikes for payment pods", "category": "ops", "icon": "?", "status": "pending", "note": "Alert SSAF"},
]

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/tasks")
def tasks():
    return jsonify(TASKS)

if __name__ == "__main__":
    app.run(port=3000)
