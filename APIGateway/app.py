# TIL ELIAS OG LAURITS: I SKAL SELV TILFØJE JERES ROUTES TIL DAMAGEREPORT OG AUTHSERVICE

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservice URLs
CARFLEET_URL = "http://carfleet-service:5003"
CUSTOMER_URL = "http://customer-information-service:5005"
CONTRACT_URL = "http://contract-service:5004"
DAMAGE_SERVICE_URL = "http://damage-report-service:5006"

# Health Check Endpoint
@app.route("/")
def home():
    return jsonify({
        "service": "API Gateway",
        "status": "running",
        "routes": ["/cars", "/customers", "/contracts", "/damagecheck"] # add auth and damagereport
    }), 200

# CAR FLEET SERVICE ROUTES
# Get all cars
@app.route("/cars", methods=["GET"])
def get_all_cars():
    try:
        response = requests.get(f"{CARFLEET_URL}/cars")
        
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add new car
@app.route("/cars", methods=["POST"])
def add_car():
    try:
        response = requests.post(f"{CARFLEET_URL}/cars", json=request.get_json())

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get car by ID
@app.route("/cars/<car_id>", methods=["GET"])
def get_car_by_id(car_id):
    try:
        response = requests.get(f"{CARFLEET_URL}/cars/{car_id}")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update car status
@app.route("/cars/<car_id>/status", methods=["PATCH"])
def update_car_status(car_id):
    try:
        response = requests.patch(f"{CARFLEET_URL}/cars/{car_id}/status", json=request.get_json())

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete car
@app.route("/cars/<car_id>", methods=["DELETE"])
def delete_car_gateway(car_id):
    try:
        response = requests.delete(f"{CARFLEET_URL}/cars/{car_id}")
        
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CUSTOMER INFORMATION SERVICE ROUTES
# Get all customers
@app.route("/customers", methods=["GET"])
def get_customers():
    try:
        response = requests.get(f"{CUSTOMER_URL}/customers")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create new customer
@app.route("/customers", methods=["POST"])
def add_customer():
    try:
        response = requests.post(f"{CUSTOMER_URL}/customers", json=request.get_json())

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get customer by ID
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    try:
        response = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get customer by email
@app.route("/customers/<email>", methods=["GET"])
def get_customer_by_email(email):
    try:
        response = requests.get(f"{CUSTOMER_URL}/customers/{email}")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete customer
@app.route("/customers/<customer_id>", methods=["DELETE"])
def delete_customer_gateway(customer_id):
    try:
        response = requests.delete(f"{CUSTOMER_URL}/customers/{customer_id}")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CONTRACT SERVICE ROUTES
# Get all contracts
@app.route("/contracts", methods=["GET"])
def get_contracts():
    try:
        response = requests.get(f"{CONTRACT_URL}/contracts")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create new contract
@app.route("/contracts", methods=["POST"])
def create_contract():
    try:
        response = requests.post(f"{CONTRACT_URL}/contracts", json=request.get_json())

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete contract
@app.route("/contracts/<int:contract_id>", methods=["DELETE"])
def delete_contract_gateway(contract_id):
    try:
        response = requests.delete(f"{CONTRACT_URL}/contracts/{contract_id}")

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# DAMAGE REPORT ROUTE
@app.route("/damagecheck", methods=["POST"])
def damage_check():

    files = []
    for file_storage in request.files.getlist("images"):
        files.append((
            "images",
            (file_storage.filename, file_storage.stream, file_storage.mimetype)
        ))

    try:
        resp = requests.post(f"{DAMAGE_SERVICE_URL}/damagecheck", files=files)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to reach damage-report-service: {e}"}), 502
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)