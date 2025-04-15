import os
import platform
import shutil
import getpass

def get_browser_cache_path(browser):
    user_profile = getpass.getuser()
    
    if platform.system() == 'Windows':
        if browser in ['chrome', 'brave']:
            cache_path = os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"
            )
            if not os.path.exists(cache_path):
                cache_path = os.path.join(
                    "C:\\Users", user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"
                )
            return cache_path
        elif browser == 'edge':
            return os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"
            )
    elif platform.system() == 'Darwin':  # macOS
        if browser in ['chrome', 'brave']:
            return os.path.join(
                "/Users", user_profile, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"
            )
        elif browser == 'edge':
            return os.path.join(
                "/Users", user_profile, "Library", "Application Support", "Microsoft", "Edge", "User Data", "Default", "Cache"
            )
    elif platform.system() == 'Linux':
        if browser in ['chrome', 'brave']:
            return os.path.join(
                "/home", user_profile, ".config", "brave-browser", "User Data", "Default", "Cache"
            )
        elif browser == 'edge':
            return os.path.join(
                "/home", user_profile, ".config", "microsoft-edge", "User Data", "Default", "Cache"
            )
        elif browser == 'firefox':
            return os.path.join(
                "/home", user_profile, ".mozilla", "firefox", "profile.default", "cache2"
            )
    elif platform.system() == 'Windows':
        if browser == 'firefox':
            return os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "Mozilla", "Firefox", "Profiles", "profile.default", "cache2"
            )
    else:
        raise Exception(f"Unsupported browser or platform: {browser}")

def extract_cache_data(browser):
    cache_path = get_browser_cache_path(browser)
    if not cache_path or not os.path.exists(cache_path):
        print(f"{browser} does not exist at {cache_path}\n")
        return None
    
    cached_files = []
    for root, dirs, files in os.walk(cache_path):
        for file in files:
            cached_files.append(os.path.join(root, file))
    
    if not cached_files:
        print(f"- {browser}.")
        return None
    
    return cached_files

def extract_cache_from_all_browsers():
    browsers = ['chrome', 'brave', 'firefox', 'edge']
    all_cache_data = {}
    
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    for browser in browsers:
        print(f"[+] {browser}...")
        cache_data = extract_cache_data(browser)
        if cache_data:
            all_cache_data[browser] = cache_data
            with open(os.path.join(cache_dir, f"{browser}_cache.txt"), "w") as file:
                for cache_file in cache_data:
                    file.write(f"{cache_file}\n")
            print(f"[+] {browser} saved.\n")
    if all_cache_data:
        print(f"Cache data has been saved in the 'cache' directory.")

extract_cache_from_all_browsers()
