from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Helper function to forward requests to services
def forward_request(method, url, json=None):
    try:
        response = requests.request(method, url, json=json, timeout=5)
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
def get_all_cars():
    return forward_request("GET", f"{CARFLEET_URL}/cars")

@app.route("/cars", methods=["POST"])
def add_car():
    return forward_request("POST", f"{CARFLEET_URL}/cars", request.get_json())

@app.route("/cars/<car_id>", methods=["GET"])
def get_car_by_id(car_id):
    return forward_request("GET", f"{CARFLEET_URL}/cars/{car_id}")

@app.route("/cars/<car_id>/status", methods=["PATCH"])
def update_car_status(car_id):
    return forward_request("PATCH", f"{CARFLEET_URL}/cars/{car_id}/status", request.get_json())


# CUSTOMER INFORMATION SERVICE ROUTES
CUSTOMER_URL = "http://customer-information-service:5005"

@app.route("/customers", methods=["GET"])
def get_customers():
    return forward_request("GET", f"{CUSTOMER_URL}/customers")

@app.route("/customers", methods=["POST"])
def add_customer_gateway():
    return forward_request("POST", f"{CUSTOMER_URL}/customers", request.get_json())

@app.route("/customers/id/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    return forward_request("GET", f"{CUSTOMER_URL}/customers/{customer_id}")

@app.route("/customers/email/<email>", methods=["GET"])
def get_customer_id_by_email(email):
    return forward_request("GET", f"{CUSTOMER_URL}/customers/{email}")


# CONTRACT SERVICE ROUTES
CONTRACT_URL = "http://contract-service:5004"

@app.route("/contracts", methods=["GET"])
def get_contracts():
    return forward_request("GET", f"{CONTRACT_URL}/contracts")

@app.route("/contracts", methods=["POST"])
def create_contract_gateway():
    return forward_request("POST", f"{CONTRACT_URL}/contracts", request.get_json())


# DAMAGE REPORT SERVICE (placeholder)
DAMAGE_URL = "http://damage-report-service:5006"

@app.route("/damages", methods=["GET"])
def get_damages():
    return forward_request("GET", f"{DAMAGE_URL}/damages")

@app.route("/damages", methods=["POST"])
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