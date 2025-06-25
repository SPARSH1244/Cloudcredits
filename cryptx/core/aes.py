from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def pad(text):
    # Pads the text to be multiple of 16 bytes (AES block size)
    while len(text) % 16 != 0:
        text += ' '
    return text

def encrypt_aes(text, password):
    key = hashlib.sha256(password.encode()).digest()  # 256-bit key
    iv = get_random_bytes(16)  # Initialization Vector
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(text)
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(iv + encrypted).decode('utf-8')  # IV is prepended

def decrypt_aes(encrypted_text, password):
    try:
        raw = base64.b64decode(encrypted_text)
        iv = raw[:16]
        ciphertext = raw[16:]
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        return decrypted.decode('utf-8').rstrip()
    except:
        return "Decryption failed. Check key or input!"
