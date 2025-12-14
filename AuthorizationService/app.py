# AuthorizationService/app.py

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import os
from db import validate_user

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    role = validate_user(username, password)

    if not role:
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=username, additional_claims={"role": role})

    return jsonify({"JWT_token": token, "token_type": "bearer", "role": role}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
