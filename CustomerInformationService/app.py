from flask import Flask, request, jsonify
from db import (
    get_all_customers,
    create_customer,
    get_customer_by_id,
    get_customer_id_by_email
)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)