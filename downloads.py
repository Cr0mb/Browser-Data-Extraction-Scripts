import sqlite3
import os
import glob
import json
import time
from datetime import datetime, timezone
import shutil

def get_browser_download_db(browser_name):
    profile_paths = {
        "chrome": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
        "brave": "~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        "edge": "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default",
        "firefox": "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
    }
    
    user_profile_path = os.path.expanduser(profile_paths.get(browser_name))
    
    if not user_profile_path:
        raise ValueError("Unsupported browser")

    if browser_name == "firefox":
        db_path = glob.glob(os.path.join(user_profile_path, "*\\places.sqlite"))
        return db_path[0] if db_path else None

    return os.path.join(user_profile_path, "History")


def copy_db_to_temp(db_path):
    if not os.path.exists(db_path):
        return None
    temp_db_path = os.path.join(os.path.dirname(db_path), "temp_history.db")
    shutil.copy(db_path, temp_db_path)
    return temp_db_path


def extract_download_history_from_browser(browser):
    download_data = []
    db_path = get_browser_download_db(browser)

    if not db_path:
        print(f"\n[-] No database found for {browser}")
        return download_data

    temp_db_path = copy_db_to_temp(db_path)
    if not temp_db_path:
        print(f"[-] Unable to copy the {browser} database")
        return download_data

    try:
        with sqlite3.connect(temp_db_path) as connection:
            cursor = connection.cursor()

            if browser in ['chrome', 'brave', 'edge']:
                query = "SELECT id, current_path, target_path, start_time, site_url FROM downloads"
            elif browser == 'firefox':
                query = "SELECT id, current_path, target_path, start_time, url FROM moz_downloads"
            else:
                raise ValueError("Unknown browser")

            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                download_info = {
                    'id': row[0],
                    'current_path': row[1],
                    'target_path': row[2],
                    'start_time': datetime.fromtimestamp(row[3] / 1000000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if row[3] else None,
                    'url': row[4],
                }
                download_data.append(download_info)

    except sqlite3.OperationalError as e:
        print(f"Error querying the {browser} database: {e}")

    return download_data


def extract_download_history_from_all_browsers():
    browsers = ['chrome', 'brave', 'edge', 'firefox']
    all_download_data = {}

    for browser in browsers:
        print(f"[+] {browser} history...")
        download_data = extract_download_history_from_browser(browser)
        if download_data:
            all_download_data[browser] = download_data
        else:
            print(f"[-] {browser} no history\n")

    return all_download_data


if __name__ == "__main__":
    # Create "downloads" directory if it doesn't exist
    download_dir = "downloads"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Extract and save data
    download_history = extract_download_history_from_all_browsers()
    output_file = os.path.join(download_dir, "download_history.json")
    
    if download_history:
        with open(output_file, "w") as f:
            json.dump(download_history, f, indent=4)
        print(f"Download history has been saved to {output_file}")
    else:
        print("No download history data found.")
