import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
import pickle

df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")
print(df.head())

# Trouve la colonne cible
target_col = None
for col in ['target', 'label', 'class']:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    raise Exception(f"Impossible de trouver la colonne cible dans le CSV. Colonnes trouvées: {df.columns.tolist()}")

# Colonnes à exclure (identifiants, texte, cible)
exclude_cols = ['FILENAME', 'URL', 'Domain', 'TLD', 'Title', target_col]
X = df.drop(columns=exclude_cols, errors='ignore')
X = X.select_dtypes(include='number')
print("Colonnes numériques utilisées:", X.columns.tolist())

y = df[target_col]

# Sélection automatique des 15 meilleurs features
k = 15
selector = SelectKBest(f_classif, k=min(k, X.shape[1]))  # gère le cas où il y a < k features
selector.fit(X, y)
selected_features = X.columns[selector.get_support()].tolist()
print("Features sélectionnées :", selected_features)

X_selected = X[selected_features]

# Split
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)
print(f"Accuracy sur le test avec les meilleures features : {score:.3f}")

with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("Modèle entraîné et sauvegardé dans model.pkl")
