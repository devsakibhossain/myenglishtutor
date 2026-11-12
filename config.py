import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Default Settings
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
DATABASE_PATH = os.getenv("DATABASE_PATH", "english_tutor.db")

# Supabase Cloud Database (Optional sync)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://earwefrgwerhbqymolef.supabase.co").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

# Validation helper
def validate_config() -> tuple[bool, str]:
    if not TELEGRAM_BOT_TOKEN:
        return False, "TELEGRAM_BOT_TOKEN is missing in .env file."
    return True, "Config is valid."
