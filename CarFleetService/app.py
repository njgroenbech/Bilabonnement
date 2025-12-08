from flask import Flask, request, jsonify
from db import get_cars, add_car, get_car_by_id
import mysql.connector
import os

app = Flask(__name__)

# standard endpoint
@app.route('/')
def home():
    return jsonify({
        "hello": "Hi there!",
        "service": "CarFleet Service",
        "status": "running"
    })

# fetches all cars
@app.route('/cars', methods=["GET"])
def cars():
    try:
        cars_list = get_cars()
        return jsonify({
            "success": True,
            "count": len(cars_list),
            "cars": cars_list
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# add car to db
@app.route('/cars/add', methods=["POST"])
def insert_car():
    try:
        data = request.get_json()
        
        brand = data.get('brand')
        model = data.get('model')
        year = data.get('year')
        license_plate = data.get('license_plate')
        km_driven = data.get('km_driven')
        fuel_type = data.get('fuel_type')
        status = data.get('status')
        purchase_price = data.get('purchase_price')
        location = data.get('location')

        add_car(brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location)

        return {
            'brand': brand,
            'model': model,
            'year': year,
            'license_plate': license_plate,
            'km_driven': km_driven,
            'fuel_type': fuel_type,
            'status': status,
            'purchase_price': purchase_price,
            'location': location
        }

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# fetches car by id
@app.route('/cars/<int:car_id>')
def fetch_car_by_id(car_id):
    try: 
        car = get_car_by_id(car_id)

        if car is None:
            return jsonify({
                "error": "Car not found"
            }), 404
        
        return jsonify(car)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)