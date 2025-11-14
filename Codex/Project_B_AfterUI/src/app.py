from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, render_template, request

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
TEST_DATA_PATH = WORKSPACE_ROOT / "test_data.json"
DEFAULT_PORT = 3000

app = Flask(
    __name__,
    static_folder=str(CURRENT_DIR / "static"),
    template_folder=str(CURRENT_DIR / "templates"),
)


def load_cases() -> Dict[str, Dict[str, Any]]:
    with TEST_DATA_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {entry["id"]: entry for entry in data}


CASES = load_cases()


def normalize_items(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prepared: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_items):
        prepared.append(
            {
                "id": item.get("id") or f"missing-{idx}",
                "title": item.get("title") or "Untitled task",
                "label": item.get("label") or "No label",
                "priority": item.get("priority") or "unknown",
                "icon": item.get("icon") or "?",
                "subtasks": item.get("subtasks") or [],
            }
        )
    return prepared


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "timestamp": time.time()}


@app.get("/")
def index() -> Any:
    case_id = request.args.get("case", "normal_density")
    case_payload = CASES.get(case_id) or list(CASES.values())[0]
    items = normalize_items(case_payload["initial_dom"].get("items", []))
    global_styles = case_payload["initial_dom"].get("global_styles", "")
    mutation = case_payload["initial_dom"].get("mutation")
    hover_required = bool(case_payload["initial_dom"].get("hover"))
    return render_template(
        "index.html",
        case_id=case_id,
        case_payload=case_payload,
        items=items,
        global_styles=global_styles,
        mutation=mutation,
        hover_required=hover_required,
    )


def run() -> None:
    port = int(os.getenv("PORT", DEFAULT_PORT))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
