from flask import Flask, request, jsonify
from db import get_cars, add_car, get_car_by_id, get_cars_by_brand, get_cars_price_per_month, get_cars_by_brand_model_status, update_car_status, delete_car 

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "hello": "Hi there!",
        "status": "running!"
    })

# endpoint for all cars
@app.route('/cars', methods=["GET"])
def cars():
    try:
        cars_list = get_cars()
        return jsonify(cars_list), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# add new car to fleet
@app.route('/cars', methods=["POST"])
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
        location = data.get('location')
        purchase_price = data.get('purchase_price')
        sub_type = data.get('sub_type')
        sub_price_per_month = data.get('sub_price_per_month')

        add_car(brand, model, year, license_plate, km_driven, fuel_type, status, location, purchase_price, sub_type, sub_price_per_month)

        return {
            'brand': brand,
            'model': model,
            'year': year,
            'license_plate': license_plate,
            'km_driven': km_driven,
            'fuel_type': fuel_type,
            'status': status,
            'location': location,
            'purchase_price': purchase_price,
            'sub_type': sub_type,
            'sub_price_per_month': sub_price_per_month,
        }

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# endpoint for car by id
@app.route('/cars/<int:car_id>', methods=["GET"])
def fetch_car_by_id(car_id):
    try: 
        car = get_car_by_id(car_id)

        if car is None:
            return jsonify({
                "error": "Car not found"
            }), 404
        
        return jsonify(car), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# endpoint for car by brand
@app.route('/cars/<string:brand>', methods=["GET"])
def fetch_car_by_brand(brand):
    try:
        car_by_brand = get_cars_by_brand(brand)

        if len(car_by_brand) == 0:
            return jsonify({
                "error": "Brand doesn't exist"
            }), 404
        
        return jsonify(car_by_brand), 200

    except Exception as e: 
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
# endpoint for cars by price
@app.route('/cars/price')
def fetch_cars_price_per_month():
    try: 
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)

        if min_price is None or max_price is None:
            return jsonify({
                "error": "Need min and max price"
            }), 400
        
        res = get_cars_price_per_month(min_price, max_price)

        return jsonify(res), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
# returns available cars matching exact specifications for contract creation
@app.route('/cars/<string:brand>/<string:model>/<int:year>/<string:fuel_type>', methods=["GET"])
def cars_for_contract_service(brand, model, year, fuel_type):
    try:
        cars_list = get_cars_by_brand_model_status(brand, model, year, fuel_type)

        return jsonify(cars_list), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# endpoint to update car status
@app.route('/cars/<int:car_id>/status', methods=["PATCH"])
def update_car_status_route(car_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        valid_status = ["available", "rented", "maintenance"]
        
        if new_status not in valid_status:
            return jsonify({
                "Success": False,
                "Error": f"Status not valid, must be one of: {valid_status}"
            }), 400
        
        update_car_status(car_id, new_status)

        return jsonify({
            "Success": True,
            "car_id": car_id,
            "status": new_status
        }), 200
    
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e)
        }), 500
    
@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car_route(car_id):
    try:
        delete_car(car_id)
        
        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)