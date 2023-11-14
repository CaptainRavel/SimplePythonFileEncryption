import os
from cryptography.fernet import Fernet
from tkinter import filedialog


class AppLogic:
    def __init__(self, ui_instance):
        # Inicjalizacja obiektu logiki aplikacji (AppLogic)
        self.ui_instance = ui_instance
        self.key_loaded = None
        self.key_file = None

    @staticmethod
    def generate_key(filename):
        # Generowanie nowego klucza szyfrującego
        key = Fernet.generate_key()
        with open(filename, 'wb') as filekey:
            filekey.write(key)
            print(f"Plik klucza '{filename}' został wygenerowany!")

    def generate_key_ui(self):
        # Wybór miejsca zapisu pliku klucza przez użytkownika
        initial_dir = os.getcwd()
        filename = filedialog.asksaveasfilename(initialdir=initial_dir, defaultextension=".key",
                                                filetypes=[("Klucz szyfrowania", "*.key")])
        if filename:
            # Wygenerowanie klucza i aktualizacja etykiety w interfejsie użytkownika
            self.generate_key(filename)
            self.ui_instance.generate_label.config(text=f"Plik klucza '{filename}' został wygenerowany!")
            self.key_file = filename
            self.key_loaded = True

    @staticmethod
    def load_key(filename):
        # Wczytanie klucza z pliku
        try:
            with open(filename, 'rb') as filekey:
                key = filekey.read()
                return Fernet(key)
        except Exception as e:
            print(f"Błąd przy wczytywaniu klucza: {e}")
            return None

    def load_key_ui(self):
        # Wybór pliku klucza do wczytania przez użytkownika
        initial_dir = os.getcwd()
        filename = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Klucz szyfrowania", "*.key")])
        if filename:
            # Wczytanie klucza i aktualizacja etykiety w interfejsie użytkownika
            loaded_key = self.load_key(filename)
            if loaded_key:
                self.ui_instance.key_label.config(text=f"Wczytano klucz: {filename}")
                self.key_loaded = True
                self.key_file = filename
            else:
                self.ui_instance.key_label.config(text="Błąd przy wczytywaniu klucza.")
                self.key_loaded = False
                self.key_file = None

    @staticmethod
    def create_encryption_folder(local_key_file):
        # Utworzenie folderu do przechowywania zaszyfrowanych plików
        key_folder = os.path.splitext(os.path.basename(local_key_file))[0] + " encrypted files"
        if not os.path.exists(key_folder):
            os.mkdir(key_folder)
        print(f"Encryption Folder: {key_folder}")
        return key_folder

    def encrypt_files(self, filenames, local_key_file):
        # Szyfrowanie plików z użyciem wczytanego klucza
        key_folder = self.create_encryption_folder(local_key_file)
        key = self.load_key(local_key_file)

        for filename in filenames:
            try:
                with open(filename, 'rb') as file_to_encrypt:
                    data = file_to_encrypt.read()
                    encrypted_data = key.encrypt(data)

                encrypted_filename = os.path.join(key_folder, os.path.basename(filename) + ".x")
                with open(encrypted_filename, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)

                print(f"Plik '{filename}' został zaszyfrowany jako '{encrypted_filename}'")
            except Exception as e:
                print(f"Błąd przy szyfrowaniu pliku '{filename}': {e}")

    def encrypt_files_ui(self):
        # Interakcja z użytkownikiem w celu wyboru plików do zaszyfrowania
        if self.key_file is not None:
            filenames = filedialog.askopenfilenames(filetypes=[("Pliki do zaszyfrowania", "*.*")])
            if filenames:
                key_folder = self.create_encryption_folder(self.key_file)
                self.encrypt_files(filenames, self.key_file)
                self.ui_instance.encrypt_label.config(
                    text=f"{len(filenames)} plików zostało zaszyfrowanych w folderze '{key_folder}'")
        else:
            self.ui_instance.encrypt_label.config(
                text="Błąd: Żaden klucz nie został wczytany. Wczytaj klucz przed próbą szyfrowania.")

    @staticmethod
    def create_decryption_folder(local_key_file):
        # Utworzenie folderu do przechowywania odszyfrowanych plików
        key_folder = os.path.splitext(os.path.basename(local_key_file))[0] + " decrypted files"
        if not os.path.exists(key_folder):
            os.mkdir(key_folder)
        return key_folder

    def decrypt_files(self, filenames, local_key_file):
        # Odszyfrowanie plików z użyciem wczytanego klucza
        key_folder = self.create_decryption_folder(local_key_file)
        key = self.load_key(local_key_file)
        decryption_error = False  # Zmienna do śledzenia błędów odszyfrowywania
        decrypted_count = 0  # Licznik odszyfrowanych plików

        for filename in filenames:
            try:
                with open(filename, 'rb') as encrypted_file:
                    encrypted_data = encrypted_file.read()
                    decrypted_data = key.decrypt(encrypted_data)

                decrypted_filename = os.path.join(key_folder, os.path.basename(filename)[:-2])
                with open(decrypted_filename, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

                print(f"Plik '{filename}' został odszyfrowany jako '{decrypted_filename}'")
                decrypted_count += 1
            except Exception as e:
                print(f"Błąd przy odszyfrowywaniu pliku '{filename}': {e}")
                decryption_error = True

        if decryption_error:
            self.ui_instance.decrypt_label.config(
                text="Błąd: Wystąpiły problemy podczas odszyfrowywania niektórych plików."
                     "Upewnij się, że używasz odpowiedniego klucza!")
        else:
            self.ui_instance.decrypt_label.config(
                text=f"{decrypted_count} plików zostało odszyfrowanych w folderze '{key_folder}'")

    def decrypt_files_ui(self):
        # Interakcja z użytkownikiem w celu wyboru plików do odszyfrowania
        if self.key_file is not None and self.key_loaded:
            filenames = filedialog.askopenfilenames(filetypes=[("Pliki do odszyfrowania", "*.x")])
            if filenames:
                self.decrypt_files(filenames, self.key_file)
        else:
            self.ui_instance.decrypt_label.config(
                text="Błąd: Żaden klucz nie został wczytany. Wczytaj klucz przed próbą odszyfrowywania.")
