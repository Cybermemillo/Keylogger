import os
import logging
from datetime import datetime
from crypto_utils import get_or_create_key, decrypt_data

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def listar_logs():
    """
    Listar los archivos de log en el directorio "Keylogger/logs" en orden cronol gico
    inverso y mostrar su informaci n por pantalla. Devuelve una lista de tuplas
    (archivo, fecha_modificación) con la información de cada archivo.

    :return: lista de tuplas (archivo, fecha_modificación)
    """
    log_path = "Keylogger/logs"
    logs = []

    for filename in os.listdir(log_path):
        if filename == "keylogger_error.log":
            continue
        file_path = os.path.join(log_path, filename)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            logs.append((filename, mod_time))

    logs.sort(key=lambda x: x[1], reverse=True)

    for idx, (filename, mod_time) in enumerate(logs, start=1):
        print(f"ID: {idx}, Archivo: {filename}, Fecha: {datetime.fromtimestamp(mod_time)}")

    return logs

def decrypt_log_file(filename):
    """
    Descifra un archivo de log cifrado con la clave almacenada en "forensic_key.json"

    :param filename: ruta del archivo de log a descifrar
    :return: None
    """
    key, _ = get_or_create_key()
    
    if not os.path.exists(filename):
        logging.error("Archivo no encontrado.")
        return

    with open(filename, "r") as f:
        encrypted_lines = f.readlines()

    logging.info("---- REGISTROS DESCIFRADOS ----")
    for encrypted_line in encrypted_lines:
        try:
            decrypted_line = decrypt_data(encrypted_line.strip(), key)
            logging.info(decrypted_line)
        except Exception as e:
            logging.error(f"No se pudo descifrar una línea: {e}")

def descifrar_log(logs):
    """
    Pide al usuario que introduzca el ID de un log que quiere descifrar y descifra
    el archivo de log correspondiente con la clave almacenada en "forensic_key.json"

    :param logs: lista de tuplas (archivo, fecha_modificación) con la información
                 de cada archivo de log
    :return: None
    """
    
    log_id = int(input("Introduce el ID del log que quieres descifrar: "))
    if 1 <= log_id <= len(logs):
        filename = logs[log_id - 1][0]
        file_path = os.path.join("Keylogger/logs", filename)
        decrypt_log_file(file_path)
    else:
        print("ID de log no válido.")

if __name__ == "__main__":
    logs = listar_logs()
    descifrar_log(logs)