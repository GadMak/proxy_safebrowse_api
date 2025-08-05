from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
import requests

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

# === Partie Signalement Discord ===
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL") or "https://discord.com/api/webhooks/1401747675845492858/UNJgNglUvTa27M-TuKEm4UqeDfl04lA0gAO0zi-MGsIczMO__eSAkcMK1JNnwTPmo509"

@app.route('/report-false-positive', methods=['POST'])
def report_false_positive():
    data = request.json
    site = data.get('site', 'Non renseigné')
    print(f"Signalement reçu pour : {site}")
    user_message = f"🚨 Faux positif signalé sur SafeBrowse AI : **{site}**"
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json={"content": user_message})
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