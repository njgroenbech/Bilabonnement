import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "customer-information-db"),
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "customer_information_db")
    )

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM customer_info')
    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return customers

def create_customer(name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('INSERT INTO customer_info (name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments)' \
    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
    (name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments))

    customer_id = cursor.lastrowid
    conn.commit()

    cursor.close()
    conn.close()

    return customer_id


