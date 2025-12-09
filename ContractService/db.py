import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "contract-db"),
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "contract_db")
    )

def get_all_contracts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM contracts")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def create_contract(customer_id, car_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contracts (customer_id, car_id, start_date, end_date)
        VALUES (%s, %s, %s, %s)
    """, (customer_id, car_id, start_date, end_date))

    conn.commit()
    contract_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return contract_id