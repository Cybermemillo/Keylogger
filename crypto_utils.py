import os
import json
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Configuración
KEY_FILE = "forensic_key.json"
SALT_SIZE = 16  # Tamaño del SALT
ITERATIONS = 100000
AES_KEY_SIZE = 32  # AES-256

def get_or_create_key():
    """ Genera una clave AES-256 única y persistente con un SALT aleatorio """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key_data = json.load(f)
            salt = base64.b64decode(key_data["salt"])
            key = base64.b64decode(key_data["key"])
            return key, salt

    # Generar SALT aleatorio
    salt = os.urandom(SALT_SIZE)
    # Generar clave AES-256 usando PBKDF2
    key = PBKDF2(os.urandom(32), salt, dkLen=AES_KEY_SIZE, count=ITERATIONS)

    # Guardar clave y SALT en archivo seguro
    with open(KEY_FILE, "w") as f:
        json.dump({
            "salt": base64.b64encode(salt).decode(),
            "key": base64.b64encode(key).decode()
        }, f)

    return key, salt

def encrypt_data(data, key):
    """ Cifra datos con AES-256 en modo EAX """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(encrypted_data, key):
    """ Descifra datos con AES-256 en modo EAX """
    data = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
