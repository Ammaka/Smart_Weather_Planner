import tkinter as tk
from ui import MyWeatherApp

if __name__ == "__main__":
    window = tk.Tk()
    app = MyWeatherApp(window)
    window.mainloop()