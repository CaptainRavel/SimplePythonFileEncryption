import tkinter as tk
from AppLogic import AppLogic


class UI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("650x200")
        self.root.update_idletasks()
        self.root.minsize(650, 200)
        self.app_logic = AppLogic(self)

        # Inicjalizacja atrybutów klasy
        self.generate_button = None
        self.generate_label = None
        self.load_button = None
        self.key_label = None
        self.encrypt_button = None
        self.encrypt_label = None
        self.decrypt_button = None
        self.decrypt_label = None

        # Utwórz widgety
        self.create_widgets(root)

    def create_widgets(self, root):
        self.generate_button = tk.Button(root, text="Generuj klucz", width=50, command=self.on_generate_key_click)
        self.generate_button.pack()
        self.generate_label = tk.Label(root, text="")
        self.generate_label.pack()
        self.load_button = tk.Button(root, text="Wczytaj klucz", width=50, command=self.on_load_key_click)
        self.load_button.pack()
        self.key_label = tk.Label(root, text="Brak wczytanego klucza")
        self.key_label.pack()
        self.encrypt_button = tk.Button(root, text="Szyfruj pliki", width=50, command=self.on_encrypt_files_click)
        self.encrypt_button.pack()
        self.encrypt_label = tk.Label(root, text="")
        self.encrypt_label.pack()
        self.decrypt_button = tk.Button(root, text="Odszyfruj pliki", width=50, command=self.on_decrypt_files_click)
        self.decrypt_button.pack()
        self.decrypt_label = tk.Label(root, text="")
        self.decrypt_label.pack()

    def on_generate_key_click(self):
        self.app_logic.generate_key_ui()

    def on_load_key_click(self):
        self.app_logic.load_key_ui()
        print(f"Key File in UI: {self.app_logic.key_file}")

    def on_encrypt_files_click(self):
        self.app_logic.encrypt_files_ui()

    def on_decrypt_files_click(self):
        self.app_logic.decrypt_files_ui()
