from flask import Flask, request, jsonify
import requests
from db import (
    get_all_contracts,
    create_contract,
    get_contract_by_id,
    delete_contract
)

app = Flask(__name__)

CUSTOMER_URL = "http://customer-information-service:5005"
CARFLEET_URL = "http://carfleet-service:5003"

# Health Check Endpoint
@app.route("/")
def home():
    return jsonify({"service": "contract-service", "status": "running"}), 200


# Get all contracts
@app.route("/contracts", methods=["GET"])
def list_contracts():
    try:
        return jsonify(get_all_contracts()), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Create new contract
@app.route("/contracts", methods=["POST"])
def create_contract_route():
    try:
        data = request.get_json()
        
        # Required fields
        required = {
            "customer_id": data.get("customer_id"),
            "car_id": data.get("car_id"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "sub_price_per_month": data.get("sub_price_per_month")
        }
        
        missing = [k for k, v in required.items() if v is None]
        if missing:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        customer_id = required["customer_id"]
        car_id = required["car_id"]

        # Validate customer exists
        customer_response = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
        if customer_response.status_code != 200:
            return jsonify({"success": False, "error": "Customer not found"}), 404

        # Validate car exists and is available
        car_response = requests.get(f"{CARFLEET_URL}/cars/{car_id}")
        if car_response.status_code != 200:
            return jsonify({"success": False, "error": "Car not found"}), 404

        car = car_response.json()
        if car.get("status") != "available":
            return jsonify({"success": False, "error": "Car is not available"}), 400

        # Update car status to rented
        update_response = requests.patch(
            f"{CARFLEET_URL}/cars/{car_id}/status",
            json={"status": "rented"}
        )
        if update_response.status_code != 200:
            return jsonify({"success": False, "error": "Failed to update car status"}), 500

        # Create contract
        contract_id = create_contract(
            customer_id,
            car_id,
            required["start_date"],
            required["end_date"],
            required["sub_price_per_month"]
        )

        return jsonify({
            "success": True,
            "contract_id": contract_id,
            "customer_id": customer_id,
            "car_id": car_id
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Delete contract and return car to available
@app.route("/contracts/<int:contract_id>", methods=["DELETE"])
def delete_contract_route(contract_id):
    try:
        contract = get_contract_by_id(contract_id)
        if not contract:
            return jsonify({"success": False, "error": "Contract not found"}), 404

        car_id = contract["car_id"]

        # Set car status back to available
        car_response = requests.patch(
            f"{CARFLEET_URL}/cars/{car_id}/status",
            json={"status": "available"}
        )
        if car_response.status_code != 200:
            return jsonify({"success": False, "error": "Failed to update car status"}), 500

        # Delete contract
        if delete_contract(contract_id):
            return jsonify({"success": True}), 200
        
        return jsonify({"success": False, "error": "Delete failed"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)