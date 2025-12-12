from flask import Flask, request, jsonify
import requests
from db import (
    get_all_customers,
    create_customer,
    get_customer_by_id,
    get_customer_id_by_email,
    delete_customer,
)

app = Flask(__name__)

CONTRACT_URL = "http://contract-service:5004"

# Health Check Endpoint
@app.route("/")
def home():
    return jsonify({"service": "customer-information-service", "status": "running"}), 200


# Get all customers
@app.route("/customers", methods=["GET"])
def customers_list():
    try:
        return jsonify(get_all_customers()), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Create new customer
@app.route("/customers", methods=["POST"])
def create_customer_route():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "Missing JSON body"}), 400

        # Required fields
        required = {
            "name": data.get("name"),
            "last_name": data.get("last_name"),
            "address": data.get("address"),
            "postal_code": data.get("postal_code"),
            "city": data.get("city"),
            "email": data.get("email"),
            "cpr_number": data.get("cpr_number"),
        }
        
        missing = [k for k, v in required.items() if v is None]
        if missing:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        # Optional fields
        registration_number = data.get("registration_number")
        account_number = data.get("account_number")
        comments = data.get("comments")

        customer_id = create_customer(
            required["name"],
            required["last_name"],
            required["address"],
            required["postal_code"],
            required["city"],
            required["email"],
            required["cpr_number"],
            registration_number,
            account_number,
            comments,
        )

        return jsonify({"success": True, "customer_id": customer_id}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Get customer by ID
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer_id_route(customer_id):
    try:
        customer = get_customer_by_id(customer_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(customer), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Get customer by email
@app.route("/customers/email/<string:email>", methods=["GET"])
def get_customer_email(email):
    try:
        customer = get_customer_id_by_email(email)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(customer), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Delete customer and all their contracts
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer_route(customer_id):
    try:
        # Get all contracts for this customer
        contracts_response = requests.get(f"{CONTRACT_URL}/contracts")
        
        if contracts_response.status_code == 200:
            contracts = contracts_response.json()
            customer_contracts = [c for c in contracts if c.get('customer_id') == customer_id]

            # Delete all customer's contracts first
            for contract in customer_contracts:
                delete_response = requests.delete(f"{CONTRACT_URL}/contracts/{contract['contract_id']}")
                if delete_response.status_code != 200:
                    return jsonify({
                        "success": False,
                        "error": f"Failed to delete contract {contract['contract_id']}"
                    }), 500

        # Delete customer
        if delete_customer(customer_id):
            return jsonify({"success": True}), 200
        
        return jsonify({"success": False, "error": "Customer not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)