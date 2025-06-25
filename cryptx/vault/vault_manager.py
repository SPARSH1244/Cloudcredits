import sqlite3
from cryptography.fernet import Fernet
import hashlib
import base64
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "vault.db")

class VaultManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = self._generate_key(master_password)
        self._init_db()

    def _generate_key(self, password):
        digest = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(digest[:32])

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    key_data TEXT
                )
            """)
            conn.commit()

    def add_key(self, name, plain_key):
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(plain_key.encode()).decode()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO keys (name, key_data) VALUES (?, ?)", (name, encrypted))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def get_key(self, name):
        fernet = Fernet(self.key)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key_data FROM keys WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return fernet.decrypt(row[0].encode()).decode()
            return None

    def get_all_keys(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM keys")
            return [row[0] for row in cursor.fetchall()]

    def delete_key(self, name):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM keys WHERE name = ?", (name,))
            conn.commit()

def try_load_vault(master_password):
    try:
        return VaultManager(master_password)
    except:
        return None
