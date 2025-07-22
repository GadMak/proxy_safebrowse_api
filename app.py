# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
from email.message import EmailMessage
import smtplib

app = Flask(__name__)
CORS(app)

# === Partie IA ===
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

# === Partie Email (toutes les infos depuis les variables d'environnement) ===
YOUR_EMAIL    = os.environ.get("YOUR_EMAIL")
SMTP_SERVER   = os.environ.get("SMTP_SERVER")
SMTP_PORT     = int(os.environ.get("SMTP_PORT", 587))
SMTP_LOGIN    = os.environ.get("SMTP_LOGIN")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

@app.route('/report-false-positive', methods=['POST'])
def report_false_positive():
    data = request.json
    site = data.get('site', 'Non renseigné')
    user_message = f"Le site {site} est signalé faux positif."
    msg = EmailMessage()
    msg['Subject'] = "Signalement Faux Positif SafeBrowse AI"
    msg['From'] = SMTP_LOGIN
    msg['To'] = YOUR_EMAIL
    msg.set_content(user_message)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.send_message(msg)
        return {"success": True}
    except Exception as e:
        print(e)
        return {"success": False, "error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
