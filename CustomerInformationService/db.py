import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "customer_information_db"),
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "customer_information_db"),
    )

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customer_info")
    customers = cursor.fetchall()

    cursor.close()
    conn.close()
    return customers

def create_customer(
    name,
    last_name,
    address,
    postal_code,
    city,
    email,
    cpr_number,
    registration_number,
    account_number,
    comments,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO customer_info 
            (name, last_name, address, postal_code, city, email, cpr_number, registration_number, account_number, comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
        (
            name,
            last_name,
            address,
            postal_code,
            city,
            email,
            cpr_number,
            registration_number,
            account_number,
            comments,
        ),
    )

    conn.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return customer_id

def get_customer_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customer_info WHERE customer_id = %s", (id,))
    customer = cursor.fetchone()

    cursor.close()
    conn.close()
    return customer

def get_customer_id_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT customer_id, name, last_name, address, postal_code, city, email, cpr_number 
        FROM customer_info WHERE email = %s
    """,
        (email,),
    )
    res = cursor.fetchone()

    cursor.close()
    conn.close()
    return res

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer_info WHERE customer_id = %s", (customer_id,))
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    return deleted > 0