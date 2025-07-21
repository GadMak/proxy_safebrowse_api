# SafeBrowse API

Ce dépôt contient le backend Python (Flask) pour l’API SafeBrowse AI :
- **Détection de sites de phishing via IA**
- **Signalement de faux positifs par les utilisateurs**
- **Endpoints Flask utilisables par une extension Chrome**

## Fonctionnalités principales

- Prédiction de phishing via endpoint `/predict`
- Signalement de faux positifs via endpoint `/report-false-positive`
- Compatible Render.com pour un déploiement cloud simple et gratuit

## Démarrage rapide (en local)

1. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
