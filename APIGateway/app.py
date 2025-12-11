from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os


app = Flask(__name__)
CORS(app)

# URL for damage-report-service; overridable via env for local testing
DAMAGE_SERVICE_URL = os.getenv("DAMAGE_SERVICE_URL", "http://damage-report-service:5006")




@app.route("/api/damage/check", methods=["POST"])
def damage_check():
    """
    Modtager billeder fra frontend og forwarder dem til DamageReportService.
    Ingen domænelogik her – kun proxy.
    """

    files = []
    for file_storage in request.files.getlist("images"):
        files.append((
            "images",
            (file_storage.filename, file_storage.stream, file_storage.mimetype)
        ))

    try:
        resp = requests.post(f"{DAMAGE_SERVICE_URL}/api/damage/check", files=files)
    except Exception as e:
        return jsonify({"error": f"Failed to reach damage-report-service: {e}"}), 502

    # Send svar uændret tilbage til frontend
    return jsonify(resp.json()), resp.status_code




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)