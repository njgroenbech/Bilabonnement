from flask import Flask, request, jsonify
from db import get_connection, get_cars
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')  # ADD THIS
def home():
    return jsonify({
        "service": "CarFleet Service",
        "status": "running",
        "version": "1.0"
    })

@app.route('/health')
def health():
    """Health check endpoint - tests DB connection"""
    try:
        conn = get_connection()
        conn.close()
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except mysql.connector.Error as err:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(err)
        }), 503

@app.route('/cars')
def cars():
    """Get all cars"""
    try:
        cars_list = get_cars()
        return jsonify({
            "success": True,
            "count": len(cars_list),
            "cars": cars_list
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)