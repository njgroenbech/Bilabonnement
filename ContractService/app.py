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


@app.route("/")
def home():
    return jsonify({"service": "contract-service", "status": "running"}), 200


# GET ALL CONTRACTS
@app.route("/contracts", methods=["GET"])
def list_contracts():
    try:
        return jsonify(get_all_contracts()), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# CREATE CONTRACT
@app.route("/contracts", methods=["POST"])
def create_contract_route():
    try:
        data = request.get_json()

        required = ["customer_id", "car_id", "start_date", "end_date", "sub_price_per_month"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

        customer_id = data["customer_id"]
        car_id = data["car_id"]

        # VALIDATE CUSTOMER
        r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
        if r.status_code != 200:
            return jsonify({"success": False, "error": "Customer not found"}), 404

        # VALIDATE CAR
        r = requests.get(f"{CARFLEET_URL}/cars/{car_id}")
        if r.status_code != 200:
            return jsonify({"success": False, "error": "Car not found"}), 404

        car = r.json()
        if car.get("status") != "available":
            return jsonify({"success": False, "error": "Car is not available"}), 400

        # UPDATE CAR STATUS → RENTED
        update_status = requests.patch(
            f"{CARFLEET_URL}/cars/{car_id}/status",
            json={"status": "rented"}
        )
        if update_status.status_code != 200:
            return jsonify({"success": False, "error": "Failed to update car status"}), 500

        # CREATE CONTRACT
        contract_id = create_contract(
            customer_id,
            car_id,
            data["start_date"],
            data["end_date"],
            data["sub_price_per_month"]
        )

        return jsonify({
            "success": True,
            "contract_id": contract_id,
            "customer_id": customer_id,
            "car_id": car_id
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# DELETE CONTRACT
@app.route("/contracts/<int:contract_id>", methods=["DELETE"])
def delete_contract_route(contract_id):
    try:
        contract = get_contract_by_id(contract_id)
        if not contract:
            return jsonify({"success": False, "error": "Contract not found"}), 404

        car_id = contract["car_id"]

        # SET CAR AVAILABLE AGAIN
        r = requests.patch(f"{CARFLEET_URL}/cars/{car_id}/status", json={"status": "available"})
        if r.status_code != 200:
            return jsonify({"success": False, "error": "Failed to update car status"}), 500

        # DELETE CONTRACT
        if delete_contract(contract_id):
            return jsonify({"success": True}), 200

        return jsonify({"success": False, "error": "Delete failed"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)