# Import
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Configuración del correo
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "salernovictoria7b@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "tmbv ucri ukqa czax")

def send_email(subject, message, recipient="salernovictoria7b@gmail.com"):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_form():
    email = request.form.get('email')  # Capturar el email
    message = request.form.get('text')  # Capturar el comentario
    if email and message:
        subject = "Nuevo feedback recibido"
        full_message = f"De: {email}\n\nMensaje:\n{message}"
        if send_email(subject, full_message):
            return redirect(url_for('success'))
        else:
            return redirect(url_for('error'))
    return redirect(url_for('error'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)