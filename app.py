from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
import requests
import datetime

app = Flask(__name__)
CORS(app)

# === Partie IA (inchangée) ===
FEATURE_COLS = [
    "URLSimilarityIndex", "CharContinuationRate", "URLCharProb", "SpacialCharRatioInURL",
    "IsHTTPS", "HasTitle", "DomainTitleMatchScore", "URLTitleMatchScore", "HasFavicon",
    "IsResponsive", "HasDescription", "HasSocialNet", "HasSubmitButton", "HasHiddenFields",
    "HasCopyrightInfo"
]

with open("model.pkl", "rb") as f:
    clf = pickle.load(f)

@app.route('/')
def home():
    return "API ML SafeBrowse OK"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = data.get("features")
    if not features or len(features) != len(FEATURE_COLS):
        return jsonify({"error": f"Veuillez envoyer {len(FEATURE_COLS)} features dans le bon ordre : {FEATURE_COLS}"}), 400

    x = np.array(features).reshape(1, -1)
    y_pred = clf.predict(x)[0]
    y_proba = clf.predict_proba(x)[0].tolist()
    result = {
        "is_phishing": int(y_pred == 1),
        "proba_phishing": y_proba[1],
        "proba_safe": y_proba[0],
        "features": features
    }
    return jsonify(result)

# === Partie Signalement Discord personnalisée ===
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route('/report-false-positive', methods=['POST'])
def report_false_positive():
    data = request.json
    site = data.get('site', 'Non renseigné')
    type_fp = data.get('type', 'autre')  # <-- "phishing", "adulte", ou autre
    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

    # Personnalisation du message
    if type_fp == "phishing":
        titre = "🛑 Phishing"
        msg = f"{titre} : le site **{site}** est signalé comme faux positif.\n🕒 {now}"
    elif type_fp == "adulte":
        titre = "🔞 Adulte"
        msg = f"{titre} : le site **{site}** est signalé comme faux positif.\n🕒 {now}"
    else:
        titre = "🚩 Autre"
        msg = f"{titre} : le site **{site}** est signalé comme faux positif.\n🕒 {now}"

    print(f"Signalement reçu pour : {site} ({now}) [{type_fp}]")
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
        if r.status_code in (200, 204):
            return jsonify({"success": True})
        else:
            print(f"Erreur Discord : {r.text}")
            return jsonify({"success": False, "error": r.text}), 500
    except Exception as e:
        print("Erreur Discord :", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)