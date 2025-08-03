# app.py
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "moods.db"

# Create table if not exists
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
init_db()

# Add a new mood
@app.route("/log", methods=["POST"])
def log_mood():
    data = request.get_json()
    mood = data.get("mood")
    reason = data.get("reason", "")
    if not mood:
        return jsonify({"error": "Mood is required"}), 400
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO moods (mood, reason) VALUES (?, ?)", (mood, reason))
    return jsonify({"message": "Mood logged successfully!"})

# Get all moods
@app.route("/logs", methods=["GET"])
def get_logs():
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("SELECT id, mood, reason, timestamp FROM moods ORDER BY timestamp DESC")
        rows = cursor.fetchall()
    logs = [{"id": r[0], "mood": r[1], "reason": r[2], "timestamp": r[3]} for r in rows]
    return jsonify(logs)

# Health check
@app.route("/", methods=["GET"])
def home():
    return "Mood Journal API is up 💖"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
