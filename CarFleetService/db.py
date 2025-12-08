import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "carfleet-db"),
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

    cursor.close()
    conn.close()

    return rows

def add_car(brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("INSERT INTO cars (brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", # 
                   (brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, location))
    
    car_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    
    return car_id

def get_car_by_id(car_id):
    conn = get_connection()
    cursor= conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,)) # comma after id to create tuple (so it works with sqlconnector)
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row

# perhaps an unnecessary func
def get_cars_by_brand(brand):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE brand = %s", (brand))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows