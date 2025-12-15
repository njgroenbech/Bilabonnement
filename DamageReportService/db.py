import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "damage-report-db"),
        user=os.getenv("MYSQL_USER", "user_db"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "damage_report_db")
    )

def create_damage_report(contract_id, car_id, overall_status, damage_level, ai_message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO damage_reports (contract_id, car_id, overall_status, damage_level, ai_message)
        VALUES (%s, %s, %s, %s, %s)
    """, (contract_id, car_id, overall_status, damage_level, ai_message))
    report_id = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()

    return report_id

def get_all_damage_reports():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM damage_reports ORDER BY created_at DESC")
    reports = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return reports