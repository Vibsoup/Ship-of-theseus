from __future__ import annotations

import csv
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESPONSES_FILE = DATA_DIR / "responses.csv"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

FIELDS = [
    "response_id",
    "submitted_at_utc",
    "object_type",
    "replacement_percent",
    "continuity",
    "appearance_preserved",
    "history_preserved",
    "function_preserved",
    "identity_rating",
    "explanation",
    "study_version",
]


def ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not RESPONSES_FILE.exists():
        with RESPONSES_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDS).writeheader()


def as_bool_string(value: object) -> str:
    return "yes" if value is True else "no"


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/responses")
def save_response():
    payload = request.get_json(silent=True) or {}

    try:
        replacement_percent = int(payload.get("replacement_percent"))
        identity_rating = int(payload.get("identity_rating"))
    except (TypeError, ValueError):
        return jsonify(error="Replacement and identity ratings must be numbers."), 400

    if replacement_percent not in range(0, 101, 10):
        return jsonify(error="Replacement must be from 0 to 100 in steps of 10."), 400
    if identity_rating < 0 or identity_rating > 100:
        return jsonify(error="Identity rating must be between 0 and 100."), 400

    allowed = {
        "object_type": {"ship", "computer", "robot"},
        "continuity": {"continuous", "interrupted"},
        "appearance_preserved": {"yes", "no"},
        "history_preserved": {"yes", "no"},
        "function_preserved": {"yes", "no"},
    }
    clean = {}
    for field, options in allowed.items():
        value = str(payload.get(field, ""))
        if value not in options:
            return jsonify(error=f"Invalid value for {field.replace('_', ' ')}."), 400
        clean[field] = value

    explanation = str(payload.get("explanation", "")).strip()
    explanation = " ".join(explanation.split())[:500]

    row = {
        "response_id": secrets.token_hex(8),
        "submitted_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **clean,
        "replacement_percent": replacement_percent,
        "identity_rating": identity_rating,
        "explanation": explanation,
        "study_version": "mvp-0.1",
    }

    ensure_data_file()
    with RESPONSES_FILE.open("a", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=FIELDS).writerow(row)

    return jsonify(message="Response saved. Thank you for contributing.", response_id=row["response_id"]), 201


@app.get("/api/summary")
def summary():
    ensure_data_file()
    with RESPONSES_FILE.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    ratings = [int(row["identity_rating"]) for row in rows]
    return jsonify(
        response_count=len(rows),
        average_identity_rating=round(sum(ratings) / len(ratings), 1) if ratings else None,
        note="Early descriptive statistics only; not a scientific conclusion.",
    )


@app.get("/download/responses.csv")
def download_responses():
    ensure_data_file()
    return send_file(RESPONSES_FILE, as_attachment=True, download_name="theseus_responses.csv", mimetype="text/csv")


if __name__ == "__main__":
    ensure_data_file()
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
