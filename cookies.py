import os
import shutil
import sqlite3
import platform
import pandas as pd
import getpass
import psutil
import subprocess

def get_cookies_path(browser):
    user = getpass.getuser()
    paths = {
        'Windows': {
            'chrome': f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies",
            'brave': f"C:\\Users\\{user}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Network\\Cookies",
            'edge': f"C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Network\\Cookies"
        },
        'Darwin': {
            'chrome': f"/Users/{user}/Library/Application Support/Google/Chrome/User Data/Default/Network/Cookies",
            'brave': f"/Users/{user}/Library/Application Support/BraveSoftware/Brave-Browser/User Data/Default/Network/Cookies",
            'edge': f"/Users/{user}/Library/Application Support/Microsoft Edge/User Data/Default/Network/Cookies"
        },
        'Linux': {
            'chrome': f"/home/{user}/.config/google-chrome/User Data/Default/Network/Cookies",
            'brave': f"/home/{user}/.config/BraveSoftware/Brave-Browser/User Data/Default/Network/Cookies",
            'edge': f"/home/{user}/.config/microsoft-edge/User Data/Default/Network/Cookies"
        }
    }
    return paths.get(platform.system(), {}).get(browser)

def is_browser_running(browser):
    return any(browser.lower() in p.info['name'].lower() for p in psutil.process_iter(attrs=['name']))

def close_browser(browser):
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if browser.lower() in p.info['name'].lower():
            subprocess.call(["taskkill", "/F", "/PID", str(p.info['pid'])], shell=True)

def extract_cookies(browser):
    path = get_cookies_path(browser)
    if not path or not os.path.exists(path): 
        return None
    if is_browser_running(browser): 
        close_browser(browser)
    
    try:
        shutil.copy2(path, "temp_cookies.db")
        conn = sqlite3.connect("temp_cookies.db")
        df = pd.read_sql_query("SELECT host_key, name, value FROM cookies", conn)
        conn.close()
        os.remove("temp_cookies.db")
        return df
    except PermissionError:
        return None

def extract_cookies_from_all():
    os.makedirs("cookies", exist_ok=True)
    for browser in ['chrome', 'brave', 'edge']:
        df = extract_cookies(browser)
        if df is not None:
            df.to_csv(f"cookies/{browser}_cookies.csv", index=False)
            print(f"Saved {browser} cookies to cookies/{browser}_cookies.csv")

# Run the extraction
extract_cookies_from_all()
