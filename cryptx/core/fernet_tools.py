from cryptography.fernet import Fernet

def generate_fernet_key():
    return Fernet.generate_key().decode()

def encrypt_fernet(key, message):
    f = Fernet(key.encode())
    return f.encrypt(message.encode()).decode()

def decrypt_fernet(key, token):
    f = Fernet(key.encode())
    return f.decrypt(token.encode()).decode()
