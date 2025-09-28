from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Pick DB based on environment
DB_URL = os.getenv("DATABASE_URL", "sqlite:///moods.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/log", methods=["POST"])
def log_mood():
    data = request.get_json()
    mood = data.get("mood")
    reason = data.get("reason", "")
    if not mood:
        return jsonify({"error": "Mood is required"}), 400
    new_mood = Mood(mood=mood, reason=reason)
    db.session.add(new_mood)
    db.session.commit()
    return jsonify({"message": "Mood logged successfully!"})

@app.route("/logs", methods=["GET"])
def get_logs():
    moods = Mood.query.order_by(Mood.timestamp.desc()).all()
    logs = [{"id": m.id, "mood": m.mood, "reason": m.reason, "timestamp": m.timestamp.isoformat()} for m in moods]
    return jsonify(logs)

@app.route("/", methods=["GET"])
def home():
    return "Mood Journal API is up 💖"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
