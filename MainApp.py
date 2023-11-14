import tkinter as tk
from UI import UI


class MainApp:
    def __init__(self):
        # Inicjalizacja głównego okna aplikacji
        self.root = tk.Tk()

        # Ustawienie tytułu okna
        self.root.title("Aplikacja Szyfrowania")

        # Inicjalizacja obiektu interfejsu użytkownika (UI)
        self.ui = UI(self.root)

        # Uruchomienie głównej pętli programu
        self.root.mainloop()


# Warunek sprawdzający, czy plik jest uruchamiany bezpośrednio (a nie importowany)
if __name__ == "__main__":
    # Utworzenie instancji klasy MainApp, co rozpocznie wykonanie programu
    app = MainApp()
