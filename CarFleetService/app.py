from flask import Flask, request, jsonify
from db import (
    get_cars,
    add_car,
    get_car_by_id,
    get_cars_by_brand,
    get_cars_price_per_month,
    get_cars_by_brand_model_status,
    update_car_status,
    delete_car,
)

app = Flask(__name__)

# Health Check Endpoint
@app.route('/')
def home():
    return jsonify({"hello": "Hi there!", "status": "running"})


# Get All Cars in fleet
@app.route('/cars', methods=["GET"])
def cars():
    try:
        return jsonify(get_cars()), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Add a new car to the fleet
@app.route('/cars', methods=["POST"])
def insert_car():
    try:
        data = request.get_json()
        
        # Required fields
        required = {
            "brand": data.get('brand'),
            "model": data.get('model'),
            "year": data.get('year'),
            "license_plate": data.get('license_plate'),
            "fuel_type": data.get('fuel_type'),
            "purchase_price": data.get('purchase_price'),
            "sub_price_per_month": data.get('sub_price_per_month'),
            "location": data.get('location'),
        }
        
        missing = [k for k, v in required.items() if v is None]
        if missing:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        # Optional fields with defaults
        km_driven = data.get('km_driven', 0)
        status = data.get('status', 'available')

        add_car(
            required['brand'], required['model'], required['year'],
            required['license_plate'], km_driven, required['fuel_type'],
            status, required['purchase_price'], required['sub_price_per_month'],
            required['location']
        )

        return jsonify({**required, "km_driven": km_driven, "status": status}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Get car by ID
@app.route('/cars/<int:car_id>', methods=["GET"])
def fetch_car_by_id(car_id):
    try:
        car = get_car_by_id(car_id)
        if not car:
            return jsonify({"error": "Car not found"}), 404
        return jsonify(car), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Get all cars by brand
@app.route('/cars/brand/<string:brand>', methods=["GET"])
def fetch_car_by_brand(brand):
    try:
        cars = get_cars_by_brand(brand)
        if not cars:
            return jsonify({"error": "Brand doesn't exist"}), 404
        return jsonify(cars), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Get cars filtered by price range
@app.route('/cars/price')
def fetch_cars_price_per_month():
    try:
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)

        if min_price is None or max_price is None:
            return jsonify({"error": "Need min and max price"}), 400
        
        return jsonify(get_cars_price_per_month(min_price, max_price)), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Get available cars matching specifications for contract creation
@app.route('/cars/<string:brand>/<string:model>/<int:year>/<string:fuel_type>', methods=["GET"])
def cars_for_contract_service(brand, model, year, fuel_type):
    try:
        cars_list = get_cars_by_brand_model_status(brand, model, year, fuel_type)
        if not cars_list:
            return jsonify({"success": False, "message": "No cars found"}), 404
        return jsonify(cars_list), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Update car status (available, rented, maintenance)
@app.route('/cars/<int:car_id>/status', methods=["PATCH"])
def update_car_status_route(car_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ["available", "rented", "maintenance"]:
            return jsonify({
                "success": False,
                "error": "Invalid status. Must be: available, rented, or maintenance"
            }), 400
        
        update_car_status(car_id, new_status)
        return jsonify({"success": True, "car_id": car_id, "status": new_status}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Delete a car from the fleet
@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car_route(car_id):
    try:
        if delete_car(car_id):
            return jsonify({"success": True}), 200
        return jsonify({"success": False, "error": "Car not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)