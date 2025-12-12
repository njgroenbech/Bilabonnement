from flask import Flask, request, jsonify
from db import get_all_contracts, create_contract, delete_contract
from contract_post_helpers import get_or_create_customer, get_available_car_id, update_car_status

app = Flask(__name__)

# test 
@app.route('/')
def home():
    return jsonify({
        "service": "contracts!!!!",
        "greeting": "hi there!!!"
    })

# endpoint for getting all contracts
@app.route('/contracts', methods=['GET'])
def get_contracts():
    try:
        return jsonify(get_all_contracts()), 200
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e)
        })

# endpoint for deleting contract (also used when deleting customer in CustomerInformationService)
@app.route('/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract_route(contract_id):
    try:
        delete_contract(contract_id)

        return jsonify({"success": True}), 200
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# endpoint for creating a new contract, communicates with both CustomerInformationService and CarFleetService to get ids
@app.route('/contracts', methods=['POST'])
def create_contract_route():
    try:
        data = request.get_json()

        # if JSON body is empty
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        # get customer_id or create customer, payload only needs email if customer exists
        customer_id = get_or_create_customer(data)

        # parameters provided for finding car
        brand = data.get('brand')
        model = data.get('model')
        year = data.get('year')
        fuel_type = data.get('fuel_type')

        # find car_id by parameters
        car_id = get_available_car_id(brand, model, year, fuel_type)

        # update the status if car is available
        update_car_status(car_id)

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