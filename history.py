import os
import shutil
import sqlite3
import platform
import pandas as pd
import getpass

def get_browser_history_path(browser):
    user_profile = getpass.getuser()
    if platform.system() == 'Windows':
        if browser in ['brave', 'chrome']:
            history_path = os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "History"
            )
            if not os.path.exists(history_path):
                history_path = os.path.join(
                    "C:\\Users", user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History"
                )
            return history_path
        elif browser == 'edge':
            return os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "History"
            )
    elif platform.system() == 'Darwin':
        if browser in ['brave', 'chrome']:
            return os.path.join(
                "/Users", user_profile, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "User Data", "Default", "History"
            )
        elif browser == 'edge':
            return os.path.join(
                "/Users", user_profile, "Library", "Application Support", "Microsoft", "Edge", "User Data", "Default", "History"
            )
    elif platform.system() == 'Linux':
        if browser in ['brave', 'chrome']:
            return os.path.join(
                "/home", user_profile, ".config", "brave-browser", "User Data", "Default", "History"
            )
        elif browser == 'edge':
            return os.path.join(
                "/home", user_profile, ".config", "microsoft-edge", "User Data", "Default", "History"
            )
    elif platform.system() == 'Firefox':
        if browser == 'firefox':
            profile_path = os.path.join(
                "/home", user_profile, ".mozilla", "firefox"
            )
            for profile_dir in os.listdir(profile_path):
                if profile_dir.endswith(".default-release"):
                    return os.path.join(profile_path, profile_dir, "places.sqlite")
    else:
        raise Exception(f"Unsupported browser: {browser}")

def extract_history(browser):
    history_path = get_browser_history_path(browser)
    if not history_path or not os.path.exists(history_path):
        print(f"Error: The specified {browser} history file does not exist at {history_path}")
        return None
    if browser in ['brave', 'chrome', 'edge']:
        temp_history_path = "temp_history.db"
        shutil.copy2(history_path, temp_history_path)
        conn = sqlite3.connect(temp_history_path)
        cursor = conn.cursor()
        query = """
        SELECT
            urls.url,
            urls.title,
            urls.visit_count,
            urls.last_visit_time
        FROM
            urls
        ORDER BY
            last_visit_time DESC;
        """
        cursor.execute(query)
        history_data = cursor.fetchall()
        df = pd.DataFrame(history_data, columns=['URL', 'Title', 'Visit Count', 'Last Visit Time'])
        df['Last Visit Time'] = df['Last Visit Time'].apply(lambda t: pd.to_datetime(t - 11644473600000000, unit='us') if t > 0 else pd.NaT)
        conn.close()
        os.remove(temp_history_path)
        return df
    elif browser == 'firefox':
        temp_history_path = "temp_places.db"
        shutil.copy2(history_path, temp_history_path)
        conn = sqlite3.connect(temp_history_path)
        cursor = conn.cursor()
        query = """
        SELECT
            moz_places.url,
            moz_places.title,
            moz_places.visit_count,
            moz_historyvisits.visit_date
        FROM
            moz_places
        JOIN
            moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
        ORDER BY
            moz_historyvisits.visit_date DESC;
        """
        cursor.execute(query)
        history_data = cursor.fetchall()
        df = pd.DataFrame(history_data, columns=['URL', 'Title', 'Visit Count', 'Last Visit Time'])
        df['Last Visit Time'] = df['Last Visit Time'].apply(lambda t: pd.to_datetime(t / 1000, unit='s'))
        conn.close()
        os.remove(temp_history_path)
        return df

def extract_history_from_all_browsers():
    if not os.path.exists('history'):
        os.makedirs('history')

    browsers = ['chrome', 'brave', 'firefox', 'edge']
    all_data = []
    for browser in browsers:
        print(f"Extracting history from {browser}...")
        df = extract_history(browser)
        if df is not None:
            all_data.append(df)
            df.to_csv(os.path.join('history', f"{browser}_history.csv"), index=False)
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(os.path.join('history', "combined_history.csv"), index=False)
        print(f"Combined history saved to history/combined_history.csv")

if __name__ == "__main__":
    extract_history_from_all_browsers()
