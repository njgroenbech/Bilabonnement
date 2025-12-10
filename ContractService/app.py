from flask import Flask, request, jsonify
from db import get_all_contracts, create_contract
import requests
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "service": "contracts",
        "greeting": "hi there"
    })

@app.route('/contracts', methods=['GET'])
def get_contracts():
    try:
        return jsonify(get_all_contracts()), 200
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e)
        })

@app.route('/contracts', methods=['POST'])
def create_contract_route():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        # get customer_id by email from customer information service
        email = data.get('email')
        customer_response = requests.get(f'http://customer-information-service:5005/customers/{email}')

        # if customer_id can't be found by email, create a new customer:
        if customer_response.status_code != 200:
            new_customer = {
                "name": data.get('name'),
                "last_name": data.get('last_name'),
                "address": data.get('address'),
                "postal_code": data.get('postal_code'),
                "city": data.get('city'),
                "email": email,
                "cpr_number": data.get('cpr_number'),
                "registration_number": data.get('registration_number'),
                "account_number": data.get('account_number'),
                "comments": data.get('comments')
            }

            create_customer_response = requests.post('http://customer-information-service:5005/customers', json = new_customer)

            # handle error if customer was not created
            if create_customer_response.status_code != 201 and create_customer_response.status_code != 200:
                return jsonify({
                    "Success": False,
                    "Error": "Failed to create customer. You need to provide name, last_name, address, postal_code, city, email, cpr_number, registration_number and account_number"
                }), 500
            
            customer_response = requests.get(f'http://customer-information-service:5005/customers/{email}')

            # check if customer retrieval was successful
            if customer_response.status_code != 200:
                return jsonify({
                    "success": False,
                    "error": "customer not found"
                })
        
        # finally, grab customer_id
        customer_id = customer_response.json()['customer_id']

        # get car_id by brand, model, fuel type and availability
        brand = data.get('brand')
        model = data.get('model')
        year = data.get('year')
        fuel_type = data.get('fuel_type')

        carfleet_response = requests.get(f'http://carfleet-service:5003/cars/{brand}/{model}/{year}/{fuel_type}')

        # if car couldn't be found with matching parameters
        if carfleet_response.status_code != 200:
            return jsonify({
                "success": False,
                "error": f"Car with attributes '{brand}', '{model}', '{year}' and '{fuel_type}' not found"
            }), 404
        
        available_cars = carfleet_response.json() # all available cars
        if len(available_cars) == 0: # check if any cars are available with adequate parameters
            return jsonify({
                "success": False,
                "error": "No available cars found"
            }), 404
        
        car_id = available_cars[0]['car_id']

        # update car status to 'rented'
        update_car_status_response = requests.patch(f'http://carfleet-service:5003/cars/{car_id}/status', json={"status": "rented"})

        # handle error if car status wasn't updated
        if update_car_status_response.status_code != 200:
            return jsonify({
                "success": False,
                "error": "failed to update car status"
            }), 500

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # finally, create the contract
        create_contract(customer_id, car_id, start_date, end_date)

        return jsonify({
            "Success": True,
            "customer_id": customer_id,
            "car_id": car_id,
            "start_date": start_date,
            "end_date": end_date
        }), 201
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)