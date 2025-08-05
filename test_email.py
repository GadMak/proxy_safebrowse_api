import smtplib
from email.message import EmailMessage

# Renseigne bien tes infos ici
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_LOGIN = "gadmakengi@gmail.com"         # Ton adresse Gmail
SMTP_PASSWORD = "ukvx zgjd qkjo kjue"         # Ton mot de passe d'application Gmail AVEC espaces
TO = "gadmakengi@gmail.com"                  # Ou une autre adresse de test

msg = EmailMessage()
msg["Subject"] = "Test App Password"
msg["From"] = SMTP_LOGIN
msg["To"] = TO
msg.set_content("Ceci est un test d'envoi depuis Python avec app password.")

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_LOGIN, SMTP_PASSWORD)
        server.send_message(msg)
    print("✅ Email envoyé avec succès !")
except Exception as e:
    print("❌ Erreur :", e)
