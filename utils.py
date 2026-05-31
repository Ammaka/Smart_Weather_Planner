import datetime


def celsius_to_fahrenheit(celsius):
    return round((celsius * 9 / 5) + 32, 1)


def ms_to_kmh(ms):
    return round(ms * 3.6)


def format_temperature(temp_c):
    temp_f = round(celsius_to_fahrenheit(temp_c))
    temp_c = round(temp_c)
    return f"{temp_c}°C  /  {temp_f}°F"


def format_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%I:%M %p")