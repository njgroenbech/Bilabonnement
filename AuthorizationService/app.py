from flask import Flask, request, jsonify
import jwt
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Read secret from environment (set via .env / docker-compose)
JWT_SECRET = os.environ.get("JWT_SECRET", "change_this_secret")
JWT_ALGORITHM = "HS256"
JWT_EXP_HOURS = int(os.environ.get("JWT_EXP_HOURS", "1"))


USERS = {
    "admin": {"password": "password", "role": "admin"},
    "user": {"password": "password", "role": "user"},
}


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username)
    if not user or user.get("password") != password:
        return jsonify({"error": "invalid credentials"}), 401

    now = datetime.utcnow()
    exp = now + timedelta(hours=JWT_EXP_HOURS)
    payload = {
        "sub": username,
        "role": user.get("role"),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify({"access_token": token, "token_type": "bearer", "expires_in": JWT_EXP_HOURS * 3600}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
