from flask import Flask, request, jsonify
from db import get_all_customers, create_customer

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "hello": "Hi there!",
        "desc": "customer info endpoint"
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

        create_customer(name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments)

        return {
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
        }
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e)
        })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
    