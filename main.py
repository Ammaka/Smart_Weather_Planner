# ============================================================
# main.py — The Entry Point
# ============================================================
# WHY THIS FILE EXISTS:
# This is the file you run to start the app. That's its only job.
# It doesn't know about colours, API calls, or widgets.
# It just does three things:
#   1. Create the window
#   2. Hand it to WeatherApp (which builds everything inside it)
#   3. Start the event loop
#
# Think of it like a restaurant:
#   main.py   = the front door (you just walk in here)
#   ui.py     = the dining room (what you see and interact with)
#   api.py    = the kitchen (does the real work behind the scenes)
#   config.py = the manager's settings book
#   utils.py  = the utility drawer in the kitchen
#
# When someone asks "how do I run this app?" the answer is always:
#   python main.py
# ============================================================

import tkinter as tk

# We import the WeatherApp class from ui.py.
# This single import pulls in the entire UI layer.
from ui import WeatherApp


# ============================================================
# THIS BLOCK IS A PYTHON BEST PRACTICE.
#
# if __name__ == "__main__":
#
# Every Python file has a built-in variable called __name__.
# When you RUN a file directly (python main.py), __name__ is
# set to the string "__main__".
# When a file is IMPORTED by another file, __name__ is set to
# the file's own name (e.g. "main").
#
# So this block means: "only run the code below if this file
# is being run directly — not if it's being imported somewhere."
#
# For a small app like this it doesn't matter much yet, but
# it's a habit every Python developer should build from day one.
# ============================================================
if __name__ == "__main__":

    # Step 1: Create the root window.
    # This is the same tk.Tk() you saw in Stage 1.
    window = tk.Tk()

    # Step 2: Pass the window into WeatherApp.
    # WeatherApp.__init__() runs immediately and builds
    # all the widgets, labels, buttons etc. inside the window.
    # We store it in `app` even though we don't use it directly —
    # this keeps the WeatherApp object alive in memory.
    app = WeatherApp(window)

    # Step 3: Start the event loop.
    # The app now lives here until the user closes the window.
    window.mainloop()