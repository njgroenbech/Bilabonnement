from flask import Flask, request, jsonify
import random
from db import create_damage_report, get_all_damage_reports

app = Flask(__name__)

DAMAGE_LEVELS = [
    {"key": "minor", "label": "MINDRE KOSMETISKE SKADER"},
    {"key": "medium", "label": "MELLEMSTORE SKADER"},
    {"key": "major", "label": "STORE SKADER"},
]

@app.route("/damagecheck", methods=["POST"])
def damagecheck():
    files = request.files.getlist("images")
    contract_id = request.form.get("contract_id")
    car_id = request.form.get("car_id")
    
    if not files:
        return jsonify({"error": "No images uploaded"}), 400
    
    if not contract_id or not car_id:
        return jsonify({"error": "Missing contract_id or car_id"}), 400
    
    # 1) Chance for uklare billeder (gul)
    if random.random() < 0.2:
        overall_status = "unclear"
        damage_level = None
        message = "Billederne vurderes uklare. Tag nye billeder og prøv igen."

    # 2) Chance for at bilen er clearet (grøn)
    elif random.random() < 0.4:
        overall_status = "clear"
        damage_level = None
        message = "Ingen skader fundet. Bilen er godkendt"

    # 3) Ellers: skade fundet (rød) med kategori
    else:
        overall_status = "damage_found"
        level = random.choice(DAMAGE_LEVELS)
        damage_level = level["key"]
        message = f"Skade fundet: {level['label']}"
    
    # gem report i database
    report_id = create_damage_report(
        contract_id=int(contract_id),
        car_id=int(car_id),
        overall_status=overall_status,
        damage_level=damage_level,
        ai_message=message
    )
    
    return jsonify({
        "report_id": report_id,
        "overall_status": overall_status,
        "color": "yellow" if overall_status == "unclear" else ("green" if overall_status == "clear" else "red"),
        "message": message,
        "damage_level": damage_level
    }), 200

@app.route("/reports", methods=["GET"])
def get_reports():
    reports = get_all_damage_reports()
    return jsonify(reports), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
