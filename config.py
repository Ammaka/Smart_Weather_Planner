from dotenv import load_dotenv
import os

load_dotenv()

#  API KEYS & URLS 
API_KEY       = os.getenv("API_KEY")
BASE_URL      = os.getenv("BASE_URL")
GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
GROQ_MODEL    = "openai/gpt-oss-120b"
MAX_TOKENS    = 1024
UNITS         = "metric"

# window
WINDOW_TITLE    = "My Weather App"
WINDOW_WIDTH    = 620
WINDOW_HEIGHT   = 780
DEFAULT_LANG    = "EN"  

# colors
COL_BG         = "#FDFAF2"
COL_SURFACE    = "#EEE9D9"
COL_TEXT       = "#1C2B3A"
COL_MUTED      = "#7A8FA6"
COL_ACCENT     = "#4A7FA5"
COL_ACCENT_ACT = "#365F7E"
COL_TEMP       = "#1B3F5E"
COL_DETAILS    = "#4A7FA5"
COL_AI_BG      = "#EAF2F8"
COL_AI_TEXT    = "#1C2B3A"

# --- FONTS ---
FONT_TITLE  = ("Helvetica", 22, "bold")
FONT_BODY   = ("Helvetica", 13)
FONT_LARGE  = ("Helvetica", 30, "bold")
FONT_MEDIUM = ("Helvetica", 14)
FONT_MONO   = ("Courier",   12)
FONT_SMALL  = ("Helvetica", 10)
FONT_BUTTON = ("Helvetica", 12, "bold")

# --- OTHER ---
REQUEST_TIMEOUT = 10
ICON_BASE_URL   = "https://openweathermap.org/img/wn/{}@2x.png"