from flask import Flask, request, jsonify
from db import get_all_customers, create_customer, get_customer_by_id, get_customer_id_by_email, delete_customer
from customer_delete_helper import delete_customer_contracts

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "hello": "Hi there!!!!",
        "desc": "customer info endpoint!!!!"
    })

@app.route('/customers', methods=["GET"])
def get_customers():
    try:
        customer_list = get_all_customers()
        return jsonify(customer_list), 200
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "error": str(e)
        })
    
@app.route('/customers', methods=["POST"])
def add_customer():
    try:
        data = request.get_json()

        name = data.get('name')
        last_name = data.get('last_name')
        address = data.get('address')
        postal_code = data.get('postal_code')
        city = data.get('city')
        email = data.get('email')
        cpr_number = data.get('cpr_number')
        registration_number = data.get('registration_number')
        account_number = data.get('account_number')
        comments = data.get('comments')

        # create_customer automatically generates id, so we make it a variable
        customer_id = create_customer(name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments)

        return {
            "customer_id": customer_id,
            "name": name,
            "last_name": last_name,
            "address": address,
            "postal_code": postal_code,
            "city": city,
            "email": email,
            "cpr_number": cpr_number,
            "registration_number": registration_number,
            "account_number": account_number,
            "comments": comments
        }, 201
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e)
        })

# fetch customer by id
@app.route('/customers/<int:customer_id>', methods=["GET"])
def customer_by_id(customer_id):
    try:
        res = get_customer_by_id(customer_id)
        if res is None:
            return jsonify({
                "Error": "Customer not found"
            }), 404

        return jsonify(res), 200

    except Exception as e:
        return jsonify({
            "Success": False,
            "error": str(e)
        })
    
# fetch customer id by email (for contract)
@app.route('/customers/<string:email>', methods=["GET"])
def id_by_email(email):
    try:
        res = get_customer_id_by_email(email)
        if res is None:
            return jsonify({
                "Error": "Customer not found"
            }), 404
        
        return jsonify(res), 200

    except Exception as e:
        return jsonify({
            "Success": False,
            "error": str(e)
        })
    
# delete customer and their associated contracts by communicating with ContractService
@app.route('/customers/<int:customer_id>', methods=["DELETE"])
def delete_customer_route(customer_id):
    try:
        customer = get_customer_by_id(customer_id)

        if customer is None:
            return jsonify({"Error": "Customer not found"}), 404
        
        # delete contracts before customer is deleted and set car to available
        delete_customer_contracts(customer_id)

        delete_customer(customer_id)
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
    