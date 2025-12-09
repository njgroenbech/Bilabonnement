import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "carfleet-db"), # second arg is to pass default value
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "carfleet_db")
    )

# function to create a list of cars
def get_cars():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True) # each row returned will be a dict

    cursor.execute("SELECT * FROM cars;")
    rows = cursor.fetchall() # fetches all rows

    cursor.close() # close cursor after query execution
    conn.close()

    return rows

def add_car(brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("INSERT INTO cars (brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", # 
                   (brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location))
    
    car_id = cursor.lastrowid
    conn.commit() # insert is temporary, commit makes it permanent
    cursor.close()
    conn.close()
    
    return car_id

def get_car_by_id(car_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,)) # comma after id to create tuple (so it works with sqlconnector)
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return row

def get_cars_by_brand(brand):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE brand = %s", (brand,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# sort car by price
def get_cars_price_per_month(min_price, max_price):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE sub_price_per_month BETWEEN %s AND %s ORDER BY sub_price_per_month ASC", (min_price, max_price))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# return cars based on brand, model and availability (for ContractService to be able write up a car without id)
def get_cars_by_brand_model_status(brand, model, year, fuel_type):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE brand = %s AND model = %s AND year = %s AND fuel_type = %s AND status = 'available'", 
                   (brand, model, year, fuel_type))
    cars = cursor.fetchall()

    cursor.close()
    conn.close()

    return cars