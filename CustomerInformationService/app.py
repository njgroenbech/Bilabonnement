from flask import Flask, request, jsonify
import requests
from db import (
    get_all_customers,
    create_customer,
    get_customer_by_id,
    get_customer_id_by_email,
    delete_customer,
)

CONTRACT_URL = "http://contract-service:5004" 

app = Flask(__name__)

# Returns all customers
@app.route("/customers", methods=["GET"])
def customers_list():
    try:
        res = get_all_customers()
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Creates a new customer
@app.route("/customers", methods=["POST"])
def create_customer_route():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Missing JSON body"
            }), 400

        required = [
            "name",
            "last_name",
            "address",
            "postal_code",
            "city",
            "email",
            "cpr_number",
        ]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({
                "success": False,
                "error": f"Missing fields: {', '.join(missing)}"
            }), 400

        customer_id = create_customer(
            data.get("name"),
            data.get("last_name"),
            data.get("address"),
            data.get("postal_code"),
            data.get("city"),
            data.get("email"),
            data.get("cpr_number"),
            data.get("registration_number"),
            data.get("account_number"),
            data.get("comments"),
        )

        return jsonify({
            "success": True,
            "customer_id": customer_id
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Returns a customer by ID
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer_id_route(customer_id):
    try:
        res = get_customer_by_id(customer_id)
        if res is None:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Returns a customer by email
@app.route("/customers/email/<string:email>", methods=["GET"])
def get_customer_email(email):
    try:
        res = get_customer_id_by_email(email)
        if res is None:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer_route(customer_id):
    try:
        # 1. Tjek om kunden har kontrakter
        contracts_response = requests.get(f"{CONTRACT_URL}/contracts")
        
        if contracts_response.status_code == 200:
            contracts = contracts_response.json()
            customer_contracts = [
                c for c in contracts 
                if c.get('customer_id') == customer_id
            ]
            
            # 2. Slet alle kundens kontrakter først
            for contract in customer_contracts:
                delete_response = requests.delete(
                    f"{CONTRACT_URL}/contracts/{contract['contract_id']}"
                )
                if delete_response.status_code != 200:
                    return jsonify({
                        "success": False, 
                        "error": f"Failed to delete contract {contract['contract_id']}"
                    }), 500
        
        # 3. Slet kunden
        success = delete_customer(customer_id)
        
        if success:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "error": "Customer not found"}), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)