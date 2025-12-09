from flask import Flask, request, jsonify
from db import get_all_contracts, create_contract
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "service": "ContractService",
        "status": "running",
        "version": "1.0"
    })

@app.route('/contracts', methods=['GET'])
def get_contracts():
    return jsonify(get_all_contracts()), 200


@app.route('/contracts', methods=['POST'])
def create_contract_route():
    data = request.get_json()

    customer_id = data.get("customer_id")
    car_id = data.get("car_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    create_contract(customer_id, car_id, start_date, end_date)

    return {
        "customer_id": customer_id,
        "car_id": car_id,
        "start_date": start_date,
        "end_date": end_date
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)