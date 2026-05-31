import requests
from config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL, MAX_TOKENS, REQUEST_TIMEOUT


def _build_prompt(weather, language):
    lang_instruction = "Respond in German." if language == "DE" else "Respond in English."

    if language == "DE":
        first_line = f"Es ist zurzeit {weather['temp_str']} in {weather['city']}.\nHier sind einige Aktivitäten, die dich interessieren könnten:"
    else:
        first_line = f"It is currently {weather['temp_str']} in {weather['city']}.\nHere are some activities that might interest you:"

    return f"""
Give 3 short activity recommendations for someone in {weather['city']}, {weather['country']} right now.

Weather: {weather['description']}, feels like {weather['feels_like']}, humidity {weather['humidity']}%, wind {weather['wind_kmh']} km/h.

Format your response EXACTLY like this — do not change the structure:

{first_line}

• [activity]
• [activity]
• [activity]

Tip: [one thing to watch out for]

{lang_instruction}
be brief max 80 words
"""

# Calls Groq and returns activity recommendation text.
def get_recommendations(weather, language="EN"):
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }
    body = {
        "model":      GROQ_MODEL,
        "messages":   [{"role": "user", "content": _build_prompt(weather, language)}],
        "max_tokens": MAX_TOKENS,
    }

    try:
        response = requests.post(GROQ_BASE_URL, headers=headers, json=body, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection. Cannot reach Groq API.")
    except requests.exceptions.Timeout:
        raise TimeoutError("Groq API took too long to respond. Try again.")

    if response.status_code == 401:
        raise RuntimeError("Invalid Groq API key. Check your .env file.")
    elif response.status_code == 429:
        raise RuntimeError("Groq rate limit reached. Wait a moment and try again.")
    elif response.status_code != 200:
        raise RuntimeError(f"Groq API error. Status code: {response.status_code}")

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected response format from Groq: {e}")