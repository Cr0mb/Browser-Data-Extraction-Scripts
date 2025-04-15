import os
import json
import platform
import getpass
import pandas as pd

def get_bookmarks_path(browser):
    user_profile = getpass.getuser()
    system = platform.system()
    
    browser_paths = {
        'Windows': {
            'brave': "C:\\Users\\{user_profile}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Bookmarks",
            'chrome': "C:\\Users\\{user_profile}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks",
            'edge': "C:\\Users\\{user_profile}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Bookmarks"
        },
        'Darwin': {
            'brave': "/Users/{user_profile}/Library/Application Support/BraveSoftware/Brave-Browser/User Data/Default/Bookmarks",
            'chrome': "/Users/{user_profile}/Library/Application Support/Google/Chrome/User Data/Default/Bookmarks",
            'edge': "/Users/{user_profile}/Library/Application Support/Microsoft Edge/User Data/Default/Bookmarks"
        },
        'Linux': {
            'brave': "/home/{user_profile}/.config/BraveSoftware/Brave-Browser/User Data/Default/Bookmarks",
            'chrome': "/home/{user_profile}/.config/google-chrome/User Data/Default/Bookmarks",
            'edge': "/home/{user_profile}/.config/microsoft-edge/User Data/Default/Bookmarks"
        }
    }

    if system in browser_paths and browser in browser_paths[system]:
        return browser_paths[system][browser].format(user_profile=user_profile)
    
    return None

def extract_bookmarks(browser, output_dir):
    bookmarks_path = get_bookmarks_path(browser)
    if not bookmarks_path or not os.path.exists(bookmarks_path):
        print(f"Error: The specified {browser} bookmarks file does not exist at {bookmarks_path}")
        return None
    
    with open(bookmarks_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    def parse_bookmarks(bookmark_folder):
        bookmarks = []
        if "children" in bookmark_folder:
            for item in bookmark_folder["children"]:
                if "url" in item:
                    bookmarks.append((item["name"], item["url"]))
                elif "children" in item:
                    bookmarks.extend(parse_bookmarks(item))
        return bookmarks

    all_bookmarks = parse_bookmarks(data["roots"]["bookmark_bar"]) + parse_bookmarks(data["roots"]["other"])

    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{browser}_bookmarks.csv")
    df = pd.DataFrame(all_bookmarks, columns=["Title", "URL"])
    df.to_csv(output_file, index=False)
    return df

def extract_bookmarks_from_all_browsers():
    output_dir = "bookmarks"
    browsers = ['chrome', 'brave', 'edge']
    for browser in browsers:
        print(f"Extracting bookmarks from {browser}...")
        df = extract_bookmarks(browser, output_dir)
        if df is not None:
            print(f"Saved {browser} bookmarks to {output_dir}/{browser}_bookmarks.csv")

extract_bookmarks_from_all_browsers()
