# ============================================================
# ui.py — The User Interface
# ============================================================
# WHY THIS FILE EXISTS:
# Everything the user SEES and INTERACTS WITH lives here.
# No API calls happen here. No data formatting happens here.
# This file's only job is to build the window and respond to
# user actions by calling the right functions from api.py.
#
# This is called the "View" in MVC (Model-View-Controller),
# a very common way of structuring applications.
# ============================================================

import tkinter as tk
from tkinter import messagebox

# Import our config values (colours, fonts, window settings)
from config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    COL_BG, COL_SURFACE, COL_TEXT, COL_MUTED,
    COL_ACCENT, COL_ACCENT_ACT, COL_TEMP, COL_DETAILS,
    FONT_TITLE, FONT_BODY, FONT_LARGE, FONT_MEDIUM,
    FONT_MONO, FONT_SMALL, FONT_BUTTON
)

# Import the API function. This is the ONLY connection between
# the UI and the internet — one clean import, one function call.
from api import get_weather


# ============================================================
# THE APP CLASS
# ============================================================
# We wrap the entire UI in a CLASS.
#
# WHY A CLASS?
# Without a class, all our widgets would be global variables
# floating around the file. With a class, they're all neatly
# stored as "self.something" — the class is like a box that
# holds all our widgets and functions together.
#
# If this is your first time seeing a class:
#   - "class WeatherApp" defines the blueprint
#   - "__init__" runs automatically when we create an instance
#   - "self" refers to THIS specific instance of the class
#   - self.whatever lets any method in the class access it
# ============================================================

class WeatherApp:

    def __init__(self, window):
        """
        Called automatically when WeatherApp() is created in main.py.
        This is where we set up the window and build all the widgets.

        Args:
            window: the tk.Tk() root window passed in from main.py
        """
        # Store the window reference so other methods can use it
        self.window = window

        # --- WINDOW CONFIGURATION ---
        self.window.title(WINDOW_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        self.window.configure(bg=COL_BG, padx=30, pady=24)

        # Now build every section of the UI.
        # We split building into separate methods so __init__ stays readable.
        # Each method is responsible for one visual section.
        self._build_header()
        self._build_search_bar()
        self._build_results_panel()
        self._build_status_bar()

        # Set the keyboard focus to the entry field so the user can
        # start typing immediately without clicking first.
        self.city_entry.focus()


    # ============================================================
    # UI BUILDER METHODS
    # Each _build_* method creates one section of the UI.
    # The underscore prefix is a Python convention meaning
    # "this is internal — don't call it from outside the class".
    # ============================================================

    def _build_header(self):
        """
        Creates the title label at the top of the window.
        Simple — just one Label widget.
        """
        title = tk.Label(
            self.window,
            text="Weather Lookup",
            font=FONT_TITLE,
            bg=COL_BG,
            fg=COL_TEXT,
        )
        # pady=(0, 20) means: 0px above, 20px below.
        # This is shorthand for setting top and bottom padding separately.
        title.pack(pady=(0, 20))


    def _build_search_bar(self):
        """
        Creates the input row: [text field] [Search button]

        We use a Frame to group these two widgets side by side.
        A Frame is an invisible container — its only job is to
        hold other widgets and control their layout.
        """
        # The Frame holds both widgets. It sits inside self.window.
        input_frame = tk.Frame(self.window, bg=COL_BG)
        input_frame.pack()

        # --- ENTRY WIDGET ---
        # An Entry is a single-line text input box.
        # We store it as self.city_entry so on_search() can read it.
        self.city_entry = tk.Entry(
            input_frame,
            width=26,
            font=FONT_BODY,
            bg=COL_SURFACE,
            fg=COL_TEXT,
            insertbackground=COL_TEXT,   # cursor colour inside the box
            relief="flat",               # no 3D border effect
            bd=8,                        # internal padding (border width)
        )
        # side="left" makes it sit on the LEFT inside the frame.
        # padx=(0, 10) adds 10px of space to its RIGHT (between it and the button).
        self.city_entry.pack(side="left", padx=(0, 10))

        # Bind the Enter/Return key to our search function.
        # "<Return>" is Tkinter's name for the Enter key.
        # lambda event: ... wraps on_search because bind() passes an event
        # argument automatically, but on_search() doesn't need one.
        self.city_entry.bind("<Return>", lambda event: self.on_search())

        # --- SEARCH BUTTON ---
        search_btn = tk.Button(
            input_frame,
            text="Search",
            command=self.on_search,      # called when clicked (no parentheses!)
            font=FONT_BUTTON,
            bg=COL_ACCENT,
            fg=COL_BG,
            activebackground=COL_ACCENT_ACT,
            activeforeground=COL_BG,
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",             # pointer cursor on hover
            bd=0,
        )
        search_btn.pack(side="left")


    def _build_results_panel(self):
        """
        Creates the results area. This is the main display.
        It contains several Label widgets that start empty
        and get updated when weather data arrives.

        We store each label as self.something so on_search()
        can update them later with .config(text=...).
        """
        # LabelFrame is like a Frame but draws a rounded border
        # and lets you set a title text on the border.
        results_frame = tk.LabelFrame(
            self.window,
            text="  Results  ",
            font=FONT_SMALL,
            bg=COL_BG,
            fg=COL_MUTED,
            bd=1,
            relief="groove",
            padx=20,
            pady=16,
        )
        # fill="x" stretches the frame to fill the full window width.
        results_frame.pack(fill="x", pady=(24, 0))

        # --- CITY NAME ---
        # Shows "Berlin, DE" once data is fetched.
        # Starts with "—" (em dash) as a placeholder.
        self.city_label = tk.Label(
            results_frame,
            text="—",
            font=FONT_MEDIUM,
            bg=COL_BG,
            fg=COL_MUTED,
        )
        self.city_label.pack()

        # --- EMOJI + TEMPERATURE ROW ---
        # We put these in a sub-Frame so they sit side by side.
        temp_row = tk.Frame(results_frame, bg=COL_BG)
        temp_row.pack(pady=(8, 4))

        self.emoji_label = tk.Label(
            temp_row,
            text="🌡️",
            font=("Helvetica", 36),   # big emoji
            bg=COL_BG,
        )
        self.emoji_label.pack(side="left", padx=(0, 12))

        self.temp_label = tk.Label(
            temp_row,
            text="— °C  /  — °F",
            font=FONT_LARGE,
            bg=COL_BG,
            fg=COL_TEMP,
        )
        self.temp_label.pack(side="left")

        # --- WEATHER DESCRIPTION ---
        # e.g. "Light rain", "Clear sky"
        self.desc_label = tk.Label(
            results_frame,
            text="Search for a city above",
            font=FONT_MEDIUM,
            bg=COL_BG,
            fg=COL_TEXT,
        )
        self.desc_label.pack(pady=(0, 16))

        # --- DETAILS PANEL ---
        # Feels like / Humidity / Wind / Pressure
        # Monospace font keeps the values lined up in a column.
        # "\n" inside the string creates line breaks.
        self.details_label = tk.Label(
            results_frame,
            text=(
                "Feels like:  —\n"
                "Humidity:    —\n"
                "Wind:        —\n"
                "Pressure:    —"
            ),
            font=FONT_MONO,
            bg=COL_BG,
            fg=COL_DETAILS,
            justify="left",     # left-align every line of the multiline text
        )
        # anchor="w" means "West" — pin this widget to the left wall
        # of its container so the text doesn't float in the centre.
        self.details_label.pack(anchor="w")


    def _build_status_bar(self):
        """
        Creates a small status bar at the bottom.
        This gives the user feedback ("Fetching...", "Error", etc.)
        without using pop-up dialogs for every little thing.
        """
        self.status_label = tk.Label(
            self.window,
            text="Enter a city name and press Search or hit Enter.",
            font=FONT_SMALL,
            bg=COL_BG,
            fg=COL_MUTED,
        )
        self.status_label.pack(pady=(16, 0))


    # ============================================================
    # EVENT HANDLER METHOD
    # This runs when the user clicks Search or presses Enter.
    # It connects the UI to the API layer.
    # ============================================================

    def on_search(self):
        """
        Called when the user triggers a search (button click or Enter key).

        Flow:
          1. Read what's in the entry field
          2. Validate it (don't search if it's empty)
          3. Show "Fetching..." status
          4. Call get_weather() from api.py
          5. On success: update all labels with the result
          6. On failure: show an error message, update status bar
        """

        # --- STEP 1: READ THE INPUT ---
        # .get() reads the current text from the Entry widget.
        # .strip() removes any accidental spaces the user may have
        # typed at the start or end. "  Berlin  " becomes "Berlin".
        city = self.city_entry.get().strip()

        # --- STEP 2: VALIDATE ---
        # Guard clause: if empty, warn and stop here.
        # We return early so the rest of the function doesn't run.
        if not city:
            messagebox.showwarning(
                "Input needed",
                "Please type a city name before searching."
            )
            return

        # --- STEP 3: SHOW "FETCHING" FEEDBACK ---
        # This is important UX. The API call below can take 1-3 seconds.
        # Without this update, the app looks frozen — the user doesn't
        # know if their click registered.
        self._set_status("Fetching weather data...")

        # update_idletasks() forces Tkinter to redraw the window RIGHT NOW,
        # before we block on the network call below.
        # Without it, the "Fetching..." text wouldn't appear until
        # after the API call finishes — too late to be useful.
        self.window.update_idletasks()

        # --- STEP 4 & 5: CALL API AND HANDLE RESULT ---
        # try/except lets us attempt something and handle failure gracefully.
        # If get_weather() raises any exception, we jump to the right except block.
        try:
            weather = get_weather(city)
            # If we reach this line, the call succeeded.
            # Update all the display labels with real data.
            self._display_weather(weather)

        except ValueError as e:
            # ValueError = city not found, or bad API key (see api.py).
            # str(e) converts the exception message to a string we can display.
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


    def _display_weather(self, weather):
        """
        Takes the weather dict returned by get_weather() and
        updates every label in the results panel.

        Args:
            weather (dict): the dict returned from api.get_weather()
                            with keys: city, country, temp_str, etc.
        """
        # .config(text=...) is how you UPDATE a label's text after
        # it's already been created. This is different from creating
        # a new label — we're changing the existing one in place.

        self.city_label.config(
            text=f"{weather['city']}, {weather['country']}",
            fg=COL_TEXT,
        )

        self.emoji_label.config(text=weather["emoji"])

        self.temp_label.config(text=weather["temp_str"])

        self.desc_label.config(text=weather["description"])

        # For details, we build a multi-line string using \n.
        # The spaces after the colons are aligned manually so the
        # values line up when using a monospace font.
        self.details_label.config(
            text=(
                f"Feels like:  {weather['feels_like']}\n"
                f"Humidity:    {weather['humidity']}%\n"
                f"Wind:        {weather['wind_kmh']} km/h\n"
                f"Pressure:    {weather['pressure']} hPa"
            )
        )

        self._set_status(f"Showing weather for: {weather['city']}, {weather['country']}")


    def _set_status(self, message):
        """
        Updates the status bar text.
        A small helper so we don't repeat .config(text=...) everywhere.

        Args:
            message (str): the status message to display
        """
        self.status_label.config(text=message)