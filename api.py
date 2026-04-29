# ============================================================
# api.py — The Internet Layer
# ============================================================
# WHY THIS FILE EXISTS:
# Everything that talks to the outside world lives here.
# The UI (ui.py) should NEVER know how data is fetched.
# It just calls get_weather("Berlin") and gets back a dict.
#
# This separation matters because:
#   - If OpenWeatherMap changes their API, you fix it HERE only
#   - You could swap to a completely different weather service
#     and ui.py would never need to change
#   - It's easier to test the API logic separately from the UI
# ============================================================

# requests is the standard Python library for making HTTP calls.
# Install it once with: pip install requests
import requests

# We import our settings from config.py so they're centralised.
# The dot before "config" means "look in the same folder as this file".
from config import API_KEY, BASE_URL, UNITS, REQUEST_TIMEOUT

# We import our helper functions from utils.py
from utils import ms_to_kmh, get_weather_emoji, format_temperature


def get_weather(city_name):
    """
    Fetches current weather data for a given city.

    This is the ONLY function the rest of the app needs to call.
    It handles the full cycle: build URL → make request →
    check for errors → parse the response → return clean data.

    Args:
        city_name (str): the city the user typed, e.g. "Berlin"

    Returns:
        dict with these keys:
            city        (str)  - confirmed city name from API
            country     (str)  - 2-letter country code, e.g. "DE"
            temp_str    (str)  - formatted "22°C / 71.6°F"
            feels_like  (str)  - formatted "20°C / 68°F"
            description (str)  - e.g. "light rain"
            emoji       (str)  - matching emoji e.g. "🌧️"
            humidity    (int)  - percentage, e.g. 78
            wind_kmh    (int)  - wind speed in km/h
            pressure    (int)  - atmospheric pressure in hPa

    Raises:
        ValueError   - if the city is not found (404 from API)
        ConnectionError - if there's no internet connection
        TimeoutError    - if the API takes too long to respond
        RuntimeError    - for any other unexpected API error
    """

    # --- STEP 1: BUILD THE REQUEST PARAMETERS ---
    # The OpenWeatherMap API accepts parameters as a dictionary.
    # requests will convert this dict into a URL query string like:
    # ?q=Berlin&appid=YOUR_KEY&units=metric
    params = {
        "q":      city_name,   # the city to look up
        "appid":  API_KEY,     # your personal API key
        "units":  UNITS,       # "metric" for Celsius
    }

    # --- STEP 2: MAKE THE HTTP REQUEST ---
    # We wrap this in try/except to catch network-level problems
    # (no internet, server unreachable, timeout, etc.)
    try:
        # requests.get() sends a GET request to the URL.
        # This is the same kind of request your browser makes
        # when you visit a webpage — just without the visual part.
        #
        # timeout= means: if we don't hear back in this many seconds,
        # stop waiting and raise a Timeout exception.
        response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)

    except requests.exceptions.ConnectionError:
        # This fires when there's no internet connection at all,
        # or the server is completely unreachable.
        raise ConnectionError("No internet connection. Please check your network.")

    except requests.exceptions.Timeout:
        # This fires when the server didn't respond within REQUEST_TIMEOUT seconds.
        raise TimeoutError("The weather API took too long to respond. Try again.")


    # --- STEP 3: CHECK THE HTTP STATUS CODE ---
    # HTTP status codes are 3-digit numbers that describe the result:
    #   200 = OK (success)
    #   401 = Unauthorised (your API key is wrong or missing)
    #   404 = Not Found (city doesn't exist in their database)
    #   429 = Too Many Requests (you've exceeded the free tier limit)
    #   500 = Internal Server Error (their problem, not yours)
    
    if response.status_code == 401:
        raise ValueError("Invalid API key. Check your key in config.py.")

    elif response.status_code == 404:
        # We use the city_name in the message so the user knows
        # exactly what wasn't found.
        raise ValueError(f"City '{city_name}' not found. Check the spelling.")

    elif response.status_code == 429:
        raise RuntimeError("API rate limit reached. Wait a minute and try again.")

    elif response.status_code != 200:
        # Catch anything else unexpected.
        raise RuntimeError(f"Unexpected API error. Status code: {response.status_code}")


    # --- STEP 4: PARSE THE JSON RESPONSE ---
    # The API returns raw JSON text. .json() converts it into
    # a nested Python dictionary we can work with.
    #
    # The OpenWeatherMap response looks like this (simplified):
    # {
    #   "name": "Berlin",
    #   "sys": { "country": "DE" },
    #   "main": {
    #     "temp": 12.4,
    #     "feels_like": 10.1,
    #     "humidity": 72,
    #     "pressure": 1013
    #   },
    #   "wind": { "speed": 5.2 },
    #   "weather": [
    #     { "description": "light rain" }
    #   ]
    # }
    data = response.json()

    # We dig into the nested structure using chained [] access.
    # data["main"]["temp"] means:
    #   → get the "main" dict from data
    #   → then get "temp" from that dict
    raw_temp       = data["main"]["temp"]
    raw_feels_like = data["main"]["feels_like"]
    humidity       = data["main"]["humidity"]
    pressure       = data["main"]["pressure"]
    wind_ms        = data["wind"]["speed"]

    # "weather" is a LIST with one item (OpenWeatherMap always
    # returns it as a list in case there are multiple conditions).
    # We grab index [0] to get the first (and usually only) item.
    description = data["weather"][0]["description"].capitalize()

    # "sys" contains metadata like country code
    country = data["sys"]["country"]

    # The API returns the city name it actually found — useful because
    # "berlin" becomes "Berlin", and typos get corrected sometimes.
    city = data["name"]


    # --- STEP 5: CLEAN UP AND RETURN ---
    # We use our util functions to format/convert values,
    # then return a clean flat dictionary.
    #
    # WHY a dictionary instead of returning raw data?
    # The UI (ui.py) should receive DISPLAY-READY data, not raw numbers.
    # It shouldn't need to know about unit conversions or formatting.
    return {
        "city":        city,
        "country":     country,
        "temp_str":    format_temperature(raw_temp),
        "feels_like":  format_temperature(raw_feels_like),
        "description": description,
        "emoji":       get_weather_emoji(description),
        "humidity":    humidity,
        "wind_kmh":    ms_to_kmh(wind_ms),
        "pressure":    pressure,
    }