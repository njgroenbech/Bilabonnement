from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

DAMAGE_LEVELS = [
    {
        "key": "minor",
        "label": "MINDRE KOSMETISKE SKADER",
        "description": "Små ridser og overfladiske skader",
    },
    {
        "key": "medium",
        "label": "MELLEMSTORE SKADER",
        "description": "Dybe ridser og større buler",
    },
    {
        "key": "major",
        "label": "STORE SKADER",
        "description": "Knuste ruder eller alvorlige mekaniske skader",
    },
]
@app.route("/api/damage/check", methods=["POST"])
def check_damage():
    """
    AI:
    - Modtager 1..n billeder (multipart/form-data, key='images')
    - Returnerer:
        overall_status: 'unclear' | 'clear' | 'damage_found'
        color: 'yellow' | 'green' | 'red'
        damage_level: én af de tre kategorier (hvis der er skade)
    """
    files = request.files.getlist("images")

    if not files:
        return jsonify({"error": "No images uploaded"}), 400

    # 1) Chance for uklare billeder (gul)
    if random.random() < 0.2:
        return jsonify({
            "overall_status": "unclear",
            "color": "yellow",
            "message": "Billederne vurderes uklare. Tag nye billeder og prøv igen.",
            "damage_level": None,
        }), 200

    # 2) Chance for at bilen er clearet (grøn)
    if random.random() < 0.4:
        return jsonify({
            "overall_status": "clear",
            "color": "green",
            "message": "Ingen skader fundet. Bilen er godkendt ",
            "damage_level": None,
        }), 200

    # 3) Ellers: skade fundet (rød) med kategori
    level = random.choice(DAMAGE_LEVELS)

    return jsonify({
        "overall_status": "damage_found",
        "color": "red",
        "message": f"Skade fundet: {level['label']} – {level['description']} ",
        "damage_level": level,
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)