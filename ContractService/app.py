from flask import Flask, request, jsonify
from db import get_connection
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "service": "ContractService",
        "status": "running",
        "version": "1.0"
    })

@app.route('/contracts', methods=['GET'])
def get_contracts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM contracts")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows), 200


@app.route('/contracts', methods=['POST'])
def create_contract():
    data = request.json

    customer_id = data.get("customer_id")
    car_id = data.get("car_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([customer_id, car_id, start_date, end_date]):
        return jsonify({"error": "Missing data"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contracts (customer_id, car_id, start_date, end_date)
        VALUES (%s, %s, %s, %s)
    """, (customer_id, car_id, start_date, end_date))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Lejeaftale oprettet",
        "contract_id": new_id
    }), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)