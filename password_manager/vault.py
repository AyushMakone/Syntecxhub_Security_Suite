import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

FILE_PATH = os.path.join(os.path.dirname(__file__), 'passwords.enc')

def _get_fernet(master_password):
    # Derive key from master password
    # In a real app, salt should be random and stored with the file.
    salt = b'syntecxhub_static_salt' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)

def _load_data(f):
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, 'rb') as file:
            encrypted = file.read()
        if not encrypted:
            return {}
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted)
    except Exception:
        # If decryption fails, password is likely wrong
        raise Exception("Invalid Master Password or Corrupt Data")

def _save_data(f, data):
    encrypted = f.encrypt(json.dumps(data).encode())
    with open(FILE_PATH, 'wb') as file:
        file.write(encrypted)

# --- Public Functions used by main.py ---

def add_entry(master_password, name, username, password):
    f = _get_fernet(master_password)
    data = _load_data(f)
    data[name] = {'username': username, 'password': password}
    _save_data(f, data)

def get_entry(master_password, name):
    f = _get_fernet(master_password)
    data = _load_data(f)
    entry = data.get(name)
    if entry:
        return f"User: {entry['username']} | Pass: {entry['password']}"
    else:
        return "Entry not found."

def delete_entry(master_password, name):
    f = _get_fernet(master_password)
    data = _load_data(f)
    if name in data:
        del data[name]
        _save_data(f, data)
    else:
        raise Exception("Entry not found.")

def search_entries(master_password, query):
    f = _get_fernet(master_password)
    data = _load_data(f)
    results = []
    for k, v in data.items():
        if query.lower() in k.lower():
            results.append(f"{k} -> {v['username']}")
    
    if not results:
        return "No matches found."
    return "\n".join(results)