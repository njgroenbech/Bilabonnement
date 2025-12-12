import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "carfleet-db"),
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "carfleet_db")
    )

def get_cars():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_car(brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, sub_price_per_month, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cars (
            brand, model, year, license_plate, km_driven,
            fuel_type, status, purchase_price, sub_price_per_month, location
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (brand, model, year, license_plate, km_driven, fuel_type, status, purchase_price, sub_price_per_month, location))
    conn.commit()
    cursor.close()
    conn.close()

def get_car_by_id(car_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
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

def get_cars_price_per_month(min_price, max_price):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars WHERE sub_price_per_month BETWEEN %s AND %s ORDER BY sub_price_per_month ASC", (min_price, max_price))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_cars_by_brand_model_status(brand, model, year, fuel_type):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars WHERE brand = %s AND model = %s AND year = %s AND fuel_type = %s AND status = 'available'", 
                   (brand, model, year, fuel_type))
    cars = cursor.fetchall()
    cursor.close()
    conn.close()
    return cars

def update_car_status(car_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE cars SET status = %s WHERE car_id = %s", (status, car_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_car(car_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE car_id = %s", (car_id,))
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    return deleted > 0