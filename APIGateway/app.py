from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, jwt_required, get_jwt

# JWT settings (must match AuthorizationService in this demo)
JWT_SECRET = "change_this_secret"

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)

# Helper function to forward requests to services
def forward_request(method, url, json=None):
    try:
        # forward incoming Authorization header if present
        headers = {}
        auth = request.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth
        response = requests.request(method, url, json=json, timeout=5, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Service unavailable: {url}"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": f"Service timeout: {url}"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Base endpoint
@app.route("/")
def home():
    return jsonify({
        "service": "API Gateway",
        "status": "running",
        "routes": [
            "/cars",
            "/customers",
            "/contracts"
        ]
    })


# CAR FLEET SERVICE ROUTES
CARFLEET_URL = "http://carfleet-service:5003"

@app.route("/cars", methods=["GET"])
@jwt_required()
def get_all_cars():
    return forward_request("GET", f"{CARFLEET_URL}/cars")

@app.route("/cars", methods=["POST"])
@jwt_required()
def add_car():
    claims = get_jwt()
    role = claims.get("role")
    if role != "admin":
        return jsonify({"error": "forbidden: admin only"}), 403
    return forward_request("POST", f"{CARFLEET_URL}/cars", request.get_json())

@app.route("/cars/<car_id>", methods=["GET"])
@jwt_required()
def get_car_by_id(car_id):
    return forward_request("GET", f"{CARFLEET_URL}/cars/{car_id}")

@app.route("/cars/<car_id>/status", methods=["PATCH"])
@jwt_required()
def update_car_status(car_id):
    return forward_request("PATCH", f"{CARFLEET_URL}/cars/{car_id}/status", request.get_json())


# CUSTOMER INFORMATION SERVICE ROUTES
CUSTOMER_URL = "http://customer-information-service:5005"

@app.route("/customers", methods=["GET"])
@jwt_required()
def get_customers():
    return forward_request("GET", f"{CUSTOMER_URL}/customers")

@app.route("/customers", methods=["POST"])
@jwt_required()
def add_customer_gateway():
    claims = get_jwt()
    role = claims.get("role")
    if role != "admin":
        return jsonify({"error": "forbidden: admin only"}), 403
    return forward_request("POST", f"{CUSTOMER_URL}/customers", request.get_json())

@app.route("/customers/id/<customer_id>", methods=["GET"])
@jwt_required()
def get_customer_by_id(customer_id):
    return forward_request("GET", f"{CUSTOMER_URL}/customers/{customer_id}")

@app.route("/customers/email/<email>", methods=["GET"])
@jwt_required()
def get_customer_id_by_email(email):
    return forward_request("GET", f"{CUSTOMER_URL}/customers/{email}")


# CONTRACT SERVICE ROUTES
CONTRACT_URL = "http://contract-service:5004"

@app.route("/contracts", methods=["GET"])
@jwt_required()
def get_contracts():
    return forward_request("GET", f"{CONTRACT_URL}/contracts")

@app.route("/contracts", methods=["POST"])
@jwt_required()
def create_contract_gateway():
    claims = get_jwt()
    role = claims.get("role")
    if role not in ("admin", "user"):
        return jsonify({"error": "forbidden"}), 403
    return forward_request("POST", f"{CONTRACT_URL}/contracts", request.get_json())


# DAMAGE REPORT SERVICE (placeholder)
DAMAGE_URL = "http://damage-report-service:5006"

@app.route("/damages", methods=["GET"])
@jwt_required()
def get_damages():
    return forward_request("GET", f"{DAMAGE_URL}/damages")

@app.route("/damages", methods=["POST"])
@jwt_required()
def add_damage():
    return forward_request("POST", f"{DAMAGE_URL}/damages", request.get_json())


# AUTH SERVICE (placeholder)
AUTH_URL = "http://authorization-service:5001"

@app.route("/auth/login", methods=["POST"])
def login():
    return forward_request("POST", f"{AUTH_URL}/login", request.get_json())


# Run gateway service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)