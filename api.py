import requests
from config import API_KEY, BASE_URL, UNITS, REQUEST_TIMEOUT
from utils import ms_to_kmh, format_temperature, format_timestamp


def get_weather(city_name):
    """Fetches current weather for a city and returns a clean dict."""
    params = {
        "q":     city_name,
        "appid": API_KEY,
        "units": UNITS,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection. Please check your network.")
    except requests.exceptions.Timeout:
        raise TimeoutError("The weather API took too long to respond. Try again.")

    if response.status_code == 401:
        raise ValueError("Invalid API key. Check your .env file.")
    elif response.status_code == 404:
        raise ValueError(f"City '{city_name}' not found. Check the spelling.")
    elif response.status_code == 429:
        raise RuntimeError("API rate limit reached. Wait a minute and try again.")
    elif response.status_code != 200:
        raise RuntimeError(f"Unexpected API error. Status code: {response.status_code}")

    data        = response.json()
    raw_temp    = data["main"]["temp"]
    raw_feels   = data["main"]["feels_like"]
    humidity    = data["main"]["humidity"]
    pressure    = data["main"]["pressure"]
    wind_ms     = data["wind"]["speed"]
    description = data["weather"][0]["description"].capitalize()
    icon_code   = data["weather"][0]["icon"]
    country     = data["sys"]["country"]
    city        = data["name"]
    sunrise_ts  = data["sys"]["sunrise"]
    sunset_ts   = data["sys"]["sunset"]

    return {
        "city":        city,
        "country":     country,
        "temp_str":    format_temperature(raw_temp),
        "feels_like":  format_temperature(raw_feels),
        "description": description,
        "icon_code":   icon_code,
        "humidity":    humidity,
        "wind_kmh":    ms_to_kmh(wind_ms),
        "pressure":    pressure,
        "sunrise":     format_timestamp(sunrise_ts),
        "sunset":      format_timestamp(sunset_ts),
    }