from flask import Flask, request, jsonify
from db import get_cars, add_car, get_car_by_id, get_cars_by_brand, get_cars_price_per_month

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "hello": "Hi there!",
        "status": "running"
    })

# fetches all cars
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

# add car to db
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

# fetch car by brand
@app.route('/cars/<string:brand>', methods=["GET"])
def fetch_car_by_brand(brand):
    try:
        car_by_brand = get_cars_by_brand(brand)

        if len(car_by_brand) == 0: # if it returns an empty list
            return jsonify({
                "error": "Brand doesn't exist"
            }), 404
        
        return jsonify(car_by_brand), 200

    except Exception as e: 
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
# fetch cars by price
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)