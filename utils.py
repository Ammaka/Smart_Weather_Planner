# ============================================================
# utils.py — Helper Functions
# ============================================================
# WHY THIS FILE EXISTS:
# Small utility functions that don't belong to the UI or the API
# but are useful across the whole project.
#
# Think of utils.py as your "toolbox" — a collection of small
# tools that solve one specific problem each, and that multiple
# other files might need.
# ============================================================


def celsius_to_fahrenheit(celsius):
    """
    Converts a Celsius temperature to Fahrenheit.

    The formula is: (C × 9/5) + 32
    We return it rounded to 1 decimal place so it looks clean.

    Args:
        celsius (float): temperature in Celsius

    Returns:
        float: temperature in Fahrenheit, rounded to 1 decimal
    
    Example:
        >>> celsius_to_fahrenheit(100)
        212.0
        >>> celsius_to_fahrenheit(0)
        32.0
    """
    return round((celsius * 9 / 5) + 32, 1)


def ms_to_kmh(ms):
    """
    Converts wind speed from metres per second (m/s) to km/h.

    OpenWeatherMap returns wind in m/s when you use metric units.
    km/h is more intuitive for most people.

    The formula is: m/s × 3.6
    (because 1 m/s = 3.6 km/h — there are 3600 seconds in an hour
    and 1000 metres in a km, so 3600/1000 = 3.6)

    Args:
        ms (float): wind speed in metres per second

    Returns:
        int: wind speed in km/h (rounded to whole number)
    """
    return round(ms * 3.6)


def get_weather_emoji(description):
    """
    Maps a weather description string to a relevant emoji.

    OpenWeatherMap returns descriptions like "clear sky",
    "light rain", "broken clouds" etc. We scan the description
    for keywords and return the best matching emoji.

    This makes the UI friendlier without needing to load image files.

    Args:
        description (str): weather description from the API
                           e.g. "light rain", "clear sky"

    Returns:
        str: a single emoji character
    """
    # .lower() converts to lowercase so "Rain" and "rain" both match.
    desc = description.lower()

    # We check for keywords in order from most specific to most general.
    # "thunderstorm" is checked before "rain" because a thunderstorm
    # IS rain — but we want the more specific emoji.
    if "thunder" in desc:
        return "⛈️"
    elif "drizzle" in desc:
        return "🌦️"
    elif "rain" in desc:
        return "🌧️"
    elif "snow" in desc:
        return "❄️"
    elif "mist" in desc or "fog" in desc or "haze" in desc:
        return "🌫️"
    elif "clear" in desc:
        return "☀️"
    elif "few clouds" in desc:
        return "🌤️"
    elif "scattered clouds" in desc:
        return "⛅"
    elif "cloud" in desc:
        return "☁️"
    else:
        # Default if nothing matches
        return "🌡️"


def format_temperature(temp_c):
    """
    Takes a Celsius float and returns a nicely formatted string
    showing both Celsius and Fahrenheit.

    Args:
        temp_c (float): temperature in Celsius

    Returns:
        str: e.g. "22°C  /  71.6°F"
    """
    temp_f = celsius_to_fahrenheit(temp_c)
    return f"{temp_c}°C  /  {temp_f}°F"