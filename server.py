from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

quotes = []

@app.route("/")
def home():
    return "🕷️ WebVerse Backend Running"

@app.route("/quotes", methods=["GET"])
def get_random_quote():
    if not quotes:
        return jsonify({"quote": "Be the first hero to drop a quote!"})
    return jsonify({"quote": random.choice(quotes)})

@app.route("/quotes", methods=["POST"])
def add_quote():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "Quote text required"}), 400
    quotes.append(text)
    return jsonify({"message": "Quote added successfully"})

if __name__ == "__main__":
    app.run()
