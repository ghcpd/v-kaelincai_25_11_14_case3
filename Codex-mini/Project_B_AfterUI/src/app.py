from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

TASKS = [
    {"title": "Audit inbound leads", "category": "Sales", "icon": "??", "status": "pending", "note": "Group for backlog"},
    {"title": "Refactor login widget with new theme", "category": "Engineering", "icon": "??", "status": "in-progress", "note": "Spacing design complete"},
    {"title": "Ship onboarding copy refresh", "category": "Design", "icon": "??", "status": "blocked", "note": "Waiting on legal"},
    {"title": "Monitor server-latency spikes", "category": "Operations", "icon": "?", "status": "pending", "note": "Add automated alert"},
    {"title": "Document scheduler upgrades", "category": "Docs", "icon": "??", "status": "in-progress", "note": "Need alignment with PM"},
]

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/tasks")
def tasks():
    return jsonify(TASKS)

if __name__ == "__main__":
    app.run(port=3000)
