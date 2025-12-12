import requests

def get_or_create_customer(json_payload):
    # If customer_id is already provided, just return it
    if 'customer_id' in json_payload:
        return json_payload['customer_id']
    
    # Otherwise, check if email is provided
    if 'email' not in json_payload:
        raise Exception("No email provided")
    
    email = json_payload['email']

    # try to get customer by email
    customer_response = requests.get(f"http://customer-information-service:5005/customers/{email}", timeout = 3)
    
    if customer_response.status_code == 200:
        return customer_response.json()["customer_id"]
    
    # create customer payload if customer id doesn't exist (expects all fields to be in payload)
    new_customer_payload = {
        "name": json_payload['name'],
        "last_name": json_payload['last_name'],
        "address": json_payload['address'],
        "postal_code": json_payload['postal_code'],
        "city": json_payload['city'],
        "email": json_payload['email'],
        "cpr_number": json_payload['cpr_number'],
        "registration_number": json_payload['registration_number'],
        "account_number": json_payload['account_number']
    }
    
    # post new customer
    create_new_customer = requests.post("http://customer-information-service:5005/customers", json=new_customer_payload, timeout = 3)

    if create_new_customer.status_code != 201:
        raise Exception("Failed to create customer")
    
    return create_new_customer.json()["customer_id"]

def get_available_car_id(brand=None, model=None, year=None, fuel_type=None, car_id=None):
    # If car_id is already provided, just return it
    if car_id:
        return car_id
    
    # Otherwise, find car by parameters
    if not all([brand, model, year, fuel_type]):
        raise Exception("Either car_id or all car parameters (brand, model, year, fuel_type) must be provided")
    
    # get car by parameters
    car_response = requests.get(f"http://carfleet-service:5003/cars/{brand}/{model}/{year}/{fuel_type}", timeout=3)
    
    if car_response.status_code != 200:
        raise Exception("Could not retrieve car_id based on parameters provided")
    
    available_cars = car_response.json()
    
    if len(available_cars) == 0:
        raise Exception("No cars available with parameters provided. Could be rented, in maintenance or the car doesn't exist.")
    
    return available_cars[0]["car_id"]

def update_car_status(car_id):
    car_status_response = requests.patch(f'http://carfleet-service:5003/cars/{car_id}/status', json={"status": "rented"}, timeout = 3)

    if car_status_response.status_code != 200:
        raise Exception(f"Failed to update car status with car_id: {car_id}")
    
    return car_status_response

