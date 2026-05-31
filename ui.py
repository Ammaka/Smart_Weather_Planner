import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

from config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_LANG,
    COL_BG, COL_SURFACE, COL_TEXT, COL_MUTED,
    COL_ACCENT, COL_ACCENT_ACT, COL_TEMP, COL_DETAILS,
    COL_AI_BG, COL_AI_TEXT,
    FONT_TITLE, FONT_BODY, FONT_LARGE, FONT_MEDIUM,
    FONT_MONO, FONT_SMALL, FONT_BUTTON,
    ICON_BASE_URL, REQUEST_TIMEOUT,
)

from api import get_weather
from ai import get_recommendations
from translations import LANGUAGES


class MyWeatherApp:

    def __init__(self, window):
        self.window = window
        self.window.title(WINDOW_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        self.window.configure(bg=COL_BG, padx=30, pady=20)

        self.last_weather = None
        self.weather_icon = None
        self.language     = DEFAULT_LANG
        self.lang         = LANGUAGES[self.language]

        self._build_header()
        self._build_search_bar()
        self._build_results_panel()
        self._build_ai_button()
        self._build_ai_panel()
        self._build_status_bar()

        self.city_entry.focus()


    def _build_header(self):
        header_frame = tk.Frame(self.window, bg=COL_BG)
        header_frame.pack(fill="x", pady=(0, 16))

        self.title_label = tk.Label(
            header_frame,
            text=self.lang["title"],
            font=FONT_TITLE,
            bg=COL_BG,
            fg=COL_TEXT,
        )
        self.title_label.pack(side="left", expand=True)

        self.lang_button = tk.Button(
            header_frame,
            text="🇩🇪 DE",
            command=self.on_toggle_language,
            font=FONT_SMALL,
            bg=COL_SURFACE,
            fg=COL_TEXT,
            activebackground=COL_ACCENT,
            activeforeground="#ffffff",
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2",
            bd=0,
        )
        self.lang_button.pack(side="right")


    def _build_search_bar(self):
        frame = tk.Frame(self.window, bg=COL_BG)
        frame.pack()

        self.city_entry = tk.Entry(
            frame,
            width=26,
            font=FONT_BODY,
            bg=COL_SURFACE,
            fg=COL_TEXT,
            insertbackground=COL_TEXT,
            relief="flat",
            bd=8,
        )
        self.city_entry.pack(side="left", padx=(0, 10))
        self.city_entry.bind("<Return>", lambda e: self.on_search())

        self.search_button = tk.Button(
            frame,
            text=self.lang["search_btn"],
            command=self.on_search,
            font=FONT_BUTTON,
            bg=COL_ACCENT,
            fg="#ffffff",
            activebackground=COL_ACCENT_ACT,
            activeforeground="#ffffff",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            bd=0,
        )
        self.search_button.pack(side="left")


    def _build_results_panel(self):
        self.results_frame = tk.LabelFrame(
            self.window,
            text=f"  {self.lang['results']}  ",
            font=FONT_SMALL,
            bg=COL_BG,
            fg=COL_MUTED,
            bd=1,
            relief="groove",
            padx=20,
            pady=12,
        )
        self.results_frame.pack(fill="x", pady=(20, 0))

        self.city_label = tk.Label(
            self.results_frame, text="—", font=FONT_MEDIUM, bg=COL_BG, fg=COL_MUTED
        )
        self.city_label.pack()

        temp_row = tk.Frame(self.results_frame, bg=COL_BG)
        temp_row.pack(pady=(8, 4))

        self.icon_label = tk.Label(temp_row, bg=COL_BG)
        self.icon_label.pack(side="left", padx=(0, 12))

        self.temp_label = tk.Label(
            temp_row,
            text="— °C  /  — °F",
            font=FONT_LARGE,
            bg=COL_BG,
            fg=COL_TEMP,
        )
        self.temp_label.pack(side="left")

        self.desc_label = tk.Label(
            self.results_frame,
            text=self.lang["no_results"],
            font=FONT_MEDIUM,
            bg=COL_BG,
            fg=COL_TEXT,
        )
        self.desc_label.pack(pady=(0, 12))

        self.details_label = tk.Label(
            self.results_frame,
            text=(
                f"{self.lang['feels_like']}:  —\n"
                f"{self.lang['humidity']}:    —\n"
                f"{self.lang['wind']}:        —\n"
                f"{self.lang['pressure']}:   —\n"
                f"{self.lang['sunrise']}:    —\n"
                f"{self.lang['sunset']}:     —"
            ),
            font=FONT_MONO,
            bg=COL_BG,
            fg=COL_DETAILS,
            justify="left",
        )
        self.details_label.pack(anchor="w")


    def _build_ai_button(self):
        self.ai_button = tk.Button(
            self.window,
            text=self.lang["ai_btn"],
            command=self.on_get_recommendations,
            font=FONT_BUTTON,
            bg=COL_SURFACE,
            fg=COL_MUTED,
            activebackground=COL_ACCENT,
            activeforeground="#ffffff",
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            bd=0,
            state="disabled",
        )
        self.ai_button.pack(pady=(14, 0))


    def _build_ai_panel(self):
        self.ai_frame = tk.LabelFrame(
            self.window,
            text=f"  {self.lang['ai_panel']}  ",
            font=FONT_SMALL,
            bg=COL_BG,
            fg=COL_MUTED,
            bd=1,
            relief="groove",
            padx=16,
            pady=12,
        )
        self.ai_frame.pack(fill="x", pady=(14, 0))

        self.ai_text = tk.Text(
            self.ai_frame,
            height=6,
            font=FONT_BODY,
            bg=COL_AI_BG,
            fg=COL_AI_TEXT,
            relief="flat",
            bd=0,
            wrap="word",
            padx=10,
            pady=8,
            state="disabled",
            cursor="arrow",
        )
        self.ai_text.pack(fill="x")


    def _build_status_bar(self):
        self.status_label = tk.Label(
            self.window,
            text=self.lang["search_hint"],
            font=FONT_SMALL,
            bg=COL_BG,
            fg=COL_MUTED,
        )
        self.status_label.pack(pady=(12, 0))


    def on_toggle_language(self):
        self.language = "DE" if self.language == "EN" else "EN"
        self.lang     = LANGUAGES[self.language]
        self.lang_button.config(
            text="🇬🇧 EN" if self.language == "DE" else "🇩🇪 DE"
        )
        self._apply_language()


    def _apply_language(self):
        self.title_label.config(text=self.lang["title"])
        self.search_button.config(text=self.lang["search_btn"])
        self.results_frame.configure(text=f"  {self.lang['results']}  ")
        self.ai_frame.configure(text=f"  {self.lang['ai_panel']}  ")
        self.ai_button.config(text=self.lang["ai_btn"])
        self.status_label.config(text=self.lang["search_hint"])

        if self.last_weather is None:
            self.desc_label.config(text=self.lang["no_results"])
            self.details_label.config(
                text=(
                    f"{self.lang['feels_like']}:  —\n"
                    f"{self.lang['humidity']}:    —\n"
                    f"{self.lang['wind']}:        —\n"
                    f"{self.lang['pressure']}:   —\n"
                    f"{self.lang['sunrise']}:    —\n"
                    f"{self.lang['sunset']}:     —"
                )
            )
        else:
            self.details_label.config(
                text=(
                    f"{self.lang['feels_like']}:  {self.last_weather['feels_like']}\n"
                    f"{self.lang['humidity']}:    {self.last_weather['humidity']}%\n"
                    f"{self.lang['wind']}:        {self.last_weather['wind_kmh']} km/h\n"
                    f"{self.lang['pressure']}:   {self.last_weather['pressure']} hPa\n"
                    f"{self.lang['sunrise']}:    {self.last_weather['sunrise']}\n"
                    f"{self.lang['sunset']}:     {self.last_weather['sunset']}"
                )
            )
        self._reset_ai_panel()


    def on_search(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning(self.lang["input_title"], self.lang["input_warning"])
            return

        self._set_status(self.lang["fetching"])
        self.window.update_idletasks()

        try:
            weather = get_weather(city)
            self.last_weather = weather
            self._display_weather(weather)
            self._load_weather_icon(weather["icon_code"])
            self.ai_button.config(state="normal", bg=COL_ACCENT, fg="#ffffff")
            self._reset_ai_panel()

        except ValueError as e:
            messagebox.showerror("Search Error", str(e))
            self._set_status(f"Error: {e}")
        except ConnectionError as e:
            messagebox.showerror("Connection Error", str(e))
            self._set_status("Error: No internet connection.")
        except TimeoutError as e:
            messagebox.showerror("Timeout", str(e))
            self._set_status("Error: Request timed out.")
        except RuntimeError as e:
            messagebox.showerror("API Error", str(e))
            self._set_status(f"API error: {e}")


    def on_get_recommendations(self):
        if self.last_weather is None:
            messagebox.showwarning(self.lang["no_data_title"], self.lang["no_data_msg"])
            return

        self._set_status(self.lang["asking_ai"])
        self.window.update_idletasks()

        try:
            recommendation = get_recommendations(self.last_weather, self.language)
            self._display_recommendations(recommendation)
            self._set_status(self.lang["rec_loaded"])

        except ConnectionError as e:
            messagebox.showerror("Connection Error", str(e))
            self._set_status("Error: No internet connection.")
        except TimeoutError as e:
            messagebox.showerror("Timeout", str(e))
            self._set_status("Error: Groq took too long.")
        except RuntimeError as e:
            messagebox.showerror("AI Error", str(e))
            self._set_status(f"AI error: {e}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", type(e).__name__ + ": " + str(e))
            self._set_status("Unexpected error occurred.")


    def _load_weather_icon(self, icon_code):
        try:
            url = ICON_BASE_URL.format(icon_code)
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            image_data = Image.open(io.BytesIO(response.content))
            image_data = image_data.resize((64, 64), Image.LANCZOS)
            self.weather_icon = ImageTk.PhotoImage(image_data)
            self.icon_label.config(image=self.weather_icon)
        except Exception:
            self.icon_label.config(image="", text="🌡️", font=("Helvetica", 36))


    def _display_weather(self, weather):
        self.city_label.config(
            text=f"{weather['city']}, {weather['country']}", fg=COL_TEXT
        )
        self.temp_label.config(text=weather["temp_str"])
        self.desc_label.config(text=weather["description"])
        self.details_label.config(
            text=(
                f"{self.lang['feels_like']}:  {weather['feels_like']}\n"
                f"{self.lang['humidity']}:    {weather['humidity']}%\n"
                f"{self.lang['wind']}:        {weather['wind_kmh']} km/h\n"
                f"{self.lang['pressure']}:   {weather['pressure']} hPa\n"
                f"{self.lang['sunrise']}:    {weather['sunrise']}\n"
                f"{self.lang['sunset']}:     {weather['sunset']}"
            )
        )
        self._set_status(f"{self.lang['showing']}: {weather['city']}, {weather['country']}")


    def _display_recommendations(self, text):
        self.ai_text.config(state="normal")
        self.ai_text.delete("1.0", "end")
        self.ai_text.insert("1.0", text)
        self.ai_text.config(state="disabled")


    def _reset_ai_panel(self):
        self.ai_text.config(state="normal")
        self.ai_text.delete("1.0", "end")
        self.ai_text.insert("1.0", self.lang["ai_placeholder"])
        self.ai_text.config(state="disabled")


    def _set_status(self, message):
        self.status_label.config(text=message)