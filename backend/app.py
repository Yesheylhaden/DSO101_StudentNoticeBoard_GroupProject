import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Allow frontend to call this API
CORS(app)

# ── DATABASE CONFIG (from environment variables) ──
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "noticeboard")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ── MODEL ──
class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(20), nullable=False, default="general")
    author = db.Column(db.String(40), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "category": self.category,
            "author": self.author,
            "date": self.date,
        }


# ── CREATE TABLES ON STARTUP ──
with app.app_context():
    db.create_all()


# ── ROUTES ──

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# GET all notices
@app.route("/announcements", methods=["GET"])
def get_notices():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notices]), 200


# POST a new notice
@app.route("/announcements", methods=["POST"])
def create_notice():
    data = request.get_json()

    # Validate required fields
    if not data or not data.get("title") or not data.get("body") or not data.get("author"):
        return jsonify({"error": "title, body, and author are required"}), 400

    # Validate category
    valid_categories = ["general", "academic", "event", "urgent", "club"]
    category = data.get("category", "general")
    if category not in valid_categories:
        return jsonify({"error": f"category must be one of {valid_categories}"}), 400

    notice = Notice(
        title=data["title"],
        body=data["body"],
        category=category,
        author=data["author"],
        date=datetime.utcnow().strftime("%d %b %Y"),
    )
    db.session.add(notice)
    db.session.commit()

    return jsonify(notice.to_dict()), 201


# UPDATE a notice by ID
@app.route("/announcements/<int:notice_id>", methods=["PUT"])
def update_notice(notice_id):
    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({"error": "Notice not found"}), 404

    data = request.get_json()

    # Update fields if provided
    if "title" in data:
        notice.title = data["title"]
    if "body" in data:
        notice.body = data["body"]
    if "category" in data:
        valid_categories = ["general", "academic", "event", "urgent", "club"]
        if data["category"] not in valid_categories:
            return jsonify({"error": f"category must be one of {valid_categories}"}), 400
        notice.category = data["category"]
    if "author" in data:
        notice.author = data["author"]

    db.session.commit()
    return jsonify(notice.to_dict()), 200


# DELETE a notice by ID
@app.route("/announcements/<int:notice_id>", methods=["DELETE"])
def delete_notice(notice_id):
    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({"error": "Notice not found"}), 404

    db.session.delete(notice)
    db.session.commit()
    return jsonify({"message": "Notice deleted"}), 200


if __name__ == "__main__":
    is_debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=5001, debug=is_debug)
