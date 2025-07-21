import pandas as pd

FEATURE_COLS = [
    "URLSimilarityIndex", "CharContinuationRate", "URLCharProb", "SpacialCharRatioInURL",
    "IsHTTPS", "HasTitle","DomainTitleMatchScore", "URLTitleMatchScore", "HasFavicon", 
    "IsResponsive", "HasDescription","HasSocialNet", "HasSubmitButton", "HasHiddenFields",
    "HasCopyrightInfo"
]

df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")
ligne = df.iloc[0]  # Prends la première ligne (mets un autre index si tu veux)

features = ligne[FEATURE_COLS].tolist()
label = ligne['label']  # ou le nom réel de la colonne cible

print("Features pour l'API :")
print(features)
print("Label réel :", label)


