from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
import random

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Create table if not exists
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/")
def home():
    return "🕷️ WebVerse Quote Backend Running"

@app.route("/quotes", methods=["GET"])
def get_random_quote():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM quotes;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return jsonify({"quote": "Be the first hero to drop a quote!"})

    random_quote = random.choice(rows)[0]
    return jsonify({"quote": random_quote})

@app.route("/quotes", methods=["POST"])
def add_quote():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Quote text required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO quotes (text) VALUES (%s);", (text,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Quote added successfully"})

if __name__ == "__main__":
    app.run()
