import dotenv
from dotenv import load_dotenv
import os       

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


UNITS = "metric"



WINDOW_TITLE  = "Weather App"
WINDOW_WIDTH  = 520
WINDOW_HEIGHT = 480



COL_BG         = "#dadae7"   # main background 
COL_SURFACE    = "#E7E7F0"   # slightly lighter surface 
COL_TEXT       = "#0B0B0B"   # main text 
COL_MUTED      = "#000000"   # secondary text 
COL_ACCENT     = "#05073a"   # buttons, highlights 
COL_ACCENT_ACT = "#05073a"   # button when pressed 
COL_TEMP       = "#05073a"   # temperature display 
COL_DETAILS    = "#0960da"   # details panel text 



FONT_TITLE   = ("Helvetica", 22, "bold")
FONT_BODY    = ("Helvetica", 13)
FONT_LARGE   = ("Helvetica", 30, "bold")
FONT_MEDIUM  = ("Helvetica", 14)
FONT_MONO    = ("Courier",   12)   
FONT_SMALL   = ("Helvetica", 10)
FONT_BUTTON  = ("Helvetica", 12, "bold")



REQUEST_TIMEOUT = 10