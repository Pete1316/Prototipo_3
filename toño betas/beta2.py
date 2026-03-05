from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
import ssl

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales del archivo .env
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = "suarez-kelvin4403@unesum.edu.ec"

# Verificar que las credenciales se cargaron
if email_sender is None or email_password is None:
    print("❌ Error: No se encontraron las variables EMAIL_SENDER o EMAIL_PASSWORD en el archivo .env")
    exit()

# Configurar el mensaje del correo
msg = MIMEText("Este es un correo de prueba enviado desde Python.")
msg["Subject"] = "Correo de Prueba"
msg["From"] = email_sender
msg["To"] = email_receiver

# Configurar el contexto SSL
context = ssl.create_default_context()

try:
    # Conectar al servidor SMTP de Gmail usando SSL (puerto 465)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())
    print("✅ Correo enviado con éxito a", email_receiver)
except Exception as e:
    print(f"❌ Error al enviar correo: {e}")
