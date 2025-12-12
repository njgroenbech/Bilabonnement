from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservice URLs
CARFLEET_URL = "http://carfleet-service:5003"
CUSTOMER_URL = "http://customer-information-service:5005"
CONTRACT_URL = "http://contract-service:5004"
DAMAGE_URL = "http://damage-report-service:5006"
AUTH_URL = "http://authorization-service:5002"

def forward_request(method, url, json=None):
    """Helper function to forward requests to microservices"""
    try:
        response = requests.request(method, url, json=json, timeout=5)
        try:
            return jsonify(response.json()), response.status_code
        except Exception:
            return jsonify({"error": response.text}), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Service unavailable: {url}"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": f"Service timeout: {url}"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health Check Endpoint
@app.route("/")
def home():
    return jsonify({
        "service": "API Gateway",
        "status": "running",
        "routes": ["/cars", "/customers", "/contracts", "/damages", "/auth"]
    }), 200


# CAR FLEET SERVICE ROUTES

# Get all cars
@app.route("/cars", methods=["GET"])
def get_all_cars():
    return forward_request("GET", f"{CARFLEET_URL}/cars")

# Add new car
@app.route("/cars", methods=["POST"])
def add_car():
    return forward_request("POST", f"{CARFLEET_URL}/cars", request.get_json())

# Get car by ID
@app.route("/cars/<car_id>", methods=["GET"])
def get_car_by_id(car_id):
    return forward_request("GET", f"{CARFLEET_URL}/cars/{car_id}")

# Update car status
@app.route("/cars/<car_id>/status", methods=["PATCH"])
def update_car_status(car_id):
    return forward_request("PATCH", f"{CARFLEET_URL}/cars/{car_id}/status", request.get_json())

# Delete car
@app.route("/cars/<car_id>", methods=["DELETE"])
def delete_car_gateway(car_id):
    return forward_request("DELETE", f"{CARFLEET_URL}/cars/{car_id}")


# CUSTOMER INFORMATION SERVICE ROUTES

# Get all customers
@app.route("/customers", methods=["GET"])
def get_customers():
    return forward_request("GET", f"{CUSTOMER_URL}/customers")

# Create new customer
@app.route("/customers", methods=["POST"])
def add_customer():
    return forward_request("POST", f"{CUSTOMER_URL}/customers", request.get_json())

# Get customer by ID
@app.route("/customers/id/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    return forward_request("GET", f"{CUSTOMER_URL}/customers/{customer_id}")

# Get customer by email
@app.route("/customers/email/<email>", methods=["GET"])
def get_customer_by_email(email):
    return forward_request("GET", f"{CUSTOMER_URL}/customers/email/{email}")

# Delete customer
@app.route("/customers/<customer_id>", methods=["DELETE"])
def delete_customer_gateway(customer_id):
    return forward_request("DELETE", f"{CUSTOMER_URL}/customers/{customer_id}")


# CONTRACT SERVICE ROUTES

# Get all contracts
@app.route("/contracts", methods=["GET"])
def get_contracts():
    return forward_request("GET", f"{CONTRACT_URL}/contracts")

# Create new contract
@app.route("/contracts", methods=["POST"])
def create_contract():
    return forward_request("POST", f"{CONTRACT_URL}/contracts", request.get_json())

# Delete contract
@app.route("/contracts/<contract_id>", methods=["DELETE"])
def delete_contract_gateway(contract_id):
    return forward_request("DELETE", f"{CONTRACT_URL}/contracts/{contract_id}")


# DAMAGE REPORT SERVICE ROUTES

# Get all damage reports
@app.route("/damages", methods=["GET"])
def get_damages():
    return forward_request("GET", f"{DAMAGE_URL}/damages")

# Create new damage report
@app.route("/damages", methods=["POST"])
def add_damage():
    return forward_request("POST", f"{DAMAGE_URL}/damages", request.get_json())


# AUTHORIZATION SERVICE ROUTES

# User login
@app.route("/auth/login", methods=["POST"])
def login():
    return forward_request("POST", f"{AUTH_URL}/login", request.get_json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)