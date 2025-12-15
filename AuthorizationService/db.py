import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "authorization-db"),
        user=os.environ.get("MYSQL_USER", "user_db"),
        password=os.environ.get("MYSQL_PASSWORD", "password"),
        database=os.environ.get("MYSQL_DB", "authorization_db")
    )

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row

def validate_user(username, password):
    user = get_user(username)
    
    if user and user.get("password") == password:
        return user.get("role")
    
    return None