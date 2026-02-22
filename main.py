from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Simulated in-memory user store (for demo purposes)
users = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com"},
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "DevSecOps Demo API",
        "version": "1.0.0",
        "status": "running"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400
    new_id = max(users.keys()) + 1
    new_user = {"id": new_id, "name": data["name"], "email": data["email"]}
    users[new_id] = new_user
    return jsonify(new_user), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
