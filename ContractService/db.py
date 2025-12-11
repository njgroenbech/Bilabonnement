import mysql.connector
import os

# DB CONNECTION
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "contract-db"),
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "contract_db"),
    )

# CONTRACT CRUD
def create_contract(customer_id, car_id, start_date, end_date, sub_price_per_month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contracts (
            customer_id,
            car_id,
            start_date,
            end_date,
            sub_price_per_month
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        customer_id,
        car_id,
        start_date,
        end_date,
        sub_price_per_month
    ))

    conn.commit()
    contract_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return contract_id


def get_all_contracts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            c.contract_id,
            c.customer_id,
            c.car_id,
            c.start_date,
            c.end_date,
            c.sub_price_per_month
        FROM contracts c
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows