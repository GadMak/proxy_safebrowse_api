from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Liste EXACTE des colonnes/features utilisées pour entraîner le modèle
FEATURE_COLS = [
    # Remplace cette liste par la tienne !
    "URLSimilarityIndex", "CharContinuationRate", "URLCharProb", "SpacialCharRatioInURL",
    "IsHTTPS", "HasTitle","DomainTitleMatchScore", "URLTitleMatchScore", "HasFavicon", 
    "IsResponsive", "HasDescription","HasSocialNet", "HasSubmitButton", "HasHiddenFields",
    "HasCopyrightInfo"
    # ... mets la liste exacte trouvée dans "Colonnes utilisées pour l'apprentissage"
]

# Charge le modèle
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)

@app.route('/')
def home():
    return "API ML SafeBrowse OK"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # --- CAS 1 : Une URL à featuriser ---
    if "url" in data:
        url = data["url"]
        # ... ICI: il faut appeler un code de featurisation pour transformer l’URL en liste de features ...
        # Pour l’instant, simule (à adapter plus tard)
        return jsonify({"error": "Feature extraction from URL not implemented in this exemple"}), 501

    # --- CAS 2 : On reçoit directement la liste de features ---
    features = data.get("features")
    if not features or len(features) != len(FEATURE_COLS):
        return jsonify({"error": f"Veuillez envoyer {len(FEATURE_COLS)} features dans le bon ordre : {FEATURE_COLS}"}), 400

    x = np.array(features).reshape(1, -1)
    y_pred = clf.predict(x)[0]
    y_proba = clf.predict_proba(x)[0].tolist()

    result = {
        "is_phishing": int(y_pred == 1),  # Ou -1 selon ton dataset (vérifie bien la valeur)
        "proba_phishing": y_proba[1],     # La proba de classe "1"
        "proba_safe": y_proba[0],         # La proba de classe "0"
        "features": features
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
