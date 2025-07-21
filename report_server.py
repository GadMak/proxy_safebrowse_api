from flask_cors import CORS
import os
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

YOUR_EMAIL = "gadmakengi@gmail.com"           # <-- Mets ici ton adresse mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_LOGIN = "gadmakengi@gmail.com"           # <-- Mets ici ton adresse Gmail
SMTP_PASSWORD = "SafeBrowse-AI2025"       # <-- Mets ici le mot de passe d’application Gmail

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
