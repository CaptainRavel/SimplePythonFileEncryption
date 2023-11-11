import tkinter as tk
from UI import UI


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplikacja Szyfrowania")
        self.ui = UI(self.root)
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
