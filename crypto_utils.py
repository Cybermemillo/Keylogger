import os
import json
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Configuración
KEY_FILE = "forensic_key.json"
SALT_SIZE = 16
ITERATIONS = 100000
AES_KEY_SIZE = 32

def get_or_create_key():
    """
    Obtiene la clave AES segura almacenada en "forensic_key.json", o la genera si no existe.
    
    :return: Una tupla (clave AES, SALT)
    """
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key_data = json.load(f)
            salt = base64.b64decode(key_data["salt"])
            key = base64.b64decode(key_data["key"])
            return key, salt
    salt = os.urandom(SALT_SIZE)
    key = PBKDF2(os.urandom(32), salt, dkLen=AES_KEY_SIZE, count=ITERATIONS)
    with open(KEY_FILE, "w") as f:
        json.dump({
            "salt": base64.b64encode(salt).decode(),
            "key": base64.b64encode(key).decode()
        }, f)

    return key, salt

def encrypt_data(data, key):
    """
    Encripta el texto plano "data" con la clave AES "key" y devuelve el resultado
    como una cadena codificada en base64.

    :param data: Texto plano a encriptar.
    :param key: Clave AES segura.
    :return: Texto cifrado en base64.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(encrypted_data, key):
    """
    Descifra el texto cifrado "encrypted_data" utilizando la clave AES "key" y devuelve
    el texto plano original.

    :param encrypted_data: Texto cifrado en base64 a descifrar.
    :param key: Clave AES segura utilizada para el descifrado.
    :return: Texto plano original descifrado.
    :raises ValueError: Si la autenticación del mensaje falla.
    """

    data = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
