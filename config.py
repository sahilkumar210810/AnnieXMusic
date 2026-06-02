import os
import requests
from datetime import datetime, timedelta

# ---------- Environment Variables ----------
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
LOGGER_ID = int(os.environ.get("LOGGER_ID", "0"))
STRING_SESSION = os.environ.get("STRING_SESSION", "")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")

# Optional APIs
DEEP_API = os.environ.get("DEEP_API", "")
API_KEY = os.environ.get("API_KEY", "")
VIDEO_API_URL = os.environ.get("VIDEO_API_URL", "")
API_URL = os.environ.get("API_URL", "")

# ---------- YouTube Cookie Configuration ----------
COOKIE_URL = os.environ.get("COOKIE_URL", "https://raw.githubusercontent.com/sahilkumar210810/AnnieXMusic/main/cookies.txt")
COOKIE_FILE = "cookies.txt"
COOKIE_EXPIRY_DAYS = 7  # Cookies expire hone par dobara download karega

def download_cookies():
    """GitHub ya Pastebin se cookies download karega"""
    try:
        response = requests.get(COOKIE_URL, timeout=10)
        if response.status_code == 200:
            with open(COOKIE_FILE, 'w') as f:
                f.write(response.text)
            print(f"[INFO] Cookies downloaded successfully from {COOKIE_URL}")
            return True
        else:
            print(f"[ERROR] Failed to download cookies. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Cookie download error: {e}")
        return False

def is_cookie_valid():
    """Check karega ki cookies file valid hai ya nahi"""
    if not os.path.exists(COOKIE_FILE):
        return False
    
    # Check file age
    file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(COOKIE_FILE))
    if file_age > timedelta(days=COOKIE_EXPIRY_DAYS):
        print(f"[INFO] Cookies file is {file_age.days} days old. Downloading fresh...")
        return False
    
    # Check file size (valid cookie file should have at least 20 lines)
    with open(COOKIE_FILE, 'r') as f:
        line_count = sum(1 for _ in f)
        if line_count < 20:
            print(f"[WARNING] Cookie file has only {line_count} lines. May be invalid.")
            return False
    
    return True

def get_cookies_file():
    """Cookies file path return karega, agar nahi hai to download karega"""
    if not is_cookie_valid():
        download_cookies()
    return COOKIE_FILE

# ---------- PO Token Configuration ----------
PO_TOKEN_URL = os.environ.get("PO_TOKEN_URL", "http://127.0.0.1:4416")
PO_TOKEN_PROVIDER = f"bgutil-http:base_url={PO_TOKEN_URL}"

# ---------- yt-dlp Options ----------
YDL_OPTS = {
    'cookiefile': get_cookies_file(),
    'format': 'bestaudio/best',
    'extractor_args': {
        'youtube': {
            'player_client': ['android'],  # Android client works best with PO Token
            'po_token': [PO_TOKEN_PROVIDER],
            'skip': ['webpage', 'configs'],  # Skip unnecessary requests
        }
    },
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': False,
    'no_warnings': False,
    'geo_bypass': True,
}

# ---------- Other Configurations ----------
DOWN_PATH = "./downloads/"
BOT_NAME = "AnnieXMusic"
BOT_VERSION = "2.0.0"
ASSISTANT_NAME = "AnnieXAssistant"
UPSTREAM_REPO = "https://github.com/sahilkumar210810/AnnieXMusic"

# MongoDB Collections
USERS_COLLECTION = "users"
CHATS_COLLECTION = "chats"
PLAYLISTS_COLLECTION = "playlists"
QUEUE_COLLECTION = "queue"

# ---------- Helper Functions ----------
def get_ydl_opts():
    """Returns fresh yt-dlp options with latest cookies"""
    return {
        **YDL_OPTS,
        'cookiefile': get_cookies_file(),
    }

# ---------- Initial Cookie Download ----------
if __name__ != "__main__":
    # Module load hone par cookies download karo
    if not os.path.exists(COOKIE_FILE):
        download_cookies()
