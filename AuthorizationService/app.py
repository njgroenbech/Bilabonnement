# AuthorizationService/app.py

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import os

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET", "dev-secret")
jwt = JWTManager(app)
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

    role = user["role"]

    # identity becomes "sub" internally; role is stored in claims
    token = create_access_token(
        identity=username,
        additional_claims={"role": role}
    )

    return jsonify({"JWT_token": token, "token_type": "bearer"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
