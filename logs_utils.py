import os
import logging
from crypto_utils import get_or_create_key, decrypt_data

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def decrypt_log_file(filename):
    """ Descifra un archivo de logs y muestra su contenido """
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

if __name__ == "__main__":
    log_file = input("Introduce el nombre del log a descifrar: ")
    decrypt_log_file(log_file)