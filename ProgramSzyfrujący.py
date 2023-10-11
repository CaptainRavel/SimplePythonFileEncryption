import tkinter as tk
import os.path as op
import cryptography as cr
from cryptography.fernet import Fernet
from tkinter import filedialog

key_loaded = None  # Zmienna do śledzenia statusu klucza
key_file = None

def generate_key(filename):
    key = Fernet.generate_key()
    with open(filename, 'wb') as filekey:
        filekey.write(key)
        print(f"Plik klucza '{filename}' został wygenerowany!\n")

def on_generate_key_click():
    filename = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Klucz szyfrowania", "*.key")])
    if filename:
        generate_key(filename)
        generate_label.config(text=f"Plik klucza '{filename}' został wygenerowany!")

def load_key(filename):
    try:
        with open(filename, 'rb') as filekey:
            key = filekey.read()
            return Fernet(key)
    except Exception as e:
        print(f"Błąd przy wczytywaniu klucza: {e}")
        return None

def on_load_key_click():
    filename = filedialog.askopenfilename(filetypes=[("Klucz szyfrowania", "*.key")])
    if filename:
        global key_loaded
        global key_file
        loaded_key = load_key(filename)
        key_file = filename
        if loaded_key:
            key_label.config(text=f"Wczytano klucz: {filename}")
            key_loaded = True  # Oznacz klucz jako wczytany
        else:
            result_label.config(text=f"Błąd przy wczytywaniu klucza.")
            key_loaded = False  # Oznacz klucz jako niewczytany (jeśli wystąpi błąd)

def encrypt_files(filenames, key):
    for filename in filenames:
        try:
            with open(filename, 'rb') as file_to_encrypt:
                data = file_to_encrypt.read()
                encrypted_data = key.encrypt(data)

            encrypted_filename = filename + ".x"
            with open(encrypted_filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

            print(f"Plik '{filename}' został zaszyfrowany jako '{encrypted_filename}'")
        except Exception as e:
            print(f"Błąd przy szyfrowaniu pliku '{filename}': {e}")

def on_encrypt_files_click():
    global key_file
    if key_file is not None:  # Sprawdzamy, czy klucz jest wczytany (nie jest None)
        key = load_key(key_file)
        if key:
            filenames = filedialog.askopenfilenames(filetypes=[("Pliki do zaszyfrowania", "*.*")])
            if filenames:
                encrypt_files(filenames, key)
                encrypt_label.config(text=f"{len(filenames)} plików zostało zaszyfrowanych!")
    else:
        encrypt_label.config(text="Błąd: Żaden klucz nie został wczytany. Wczytaj klucz przed próbą szyfrowania.")

def decrypt_files(filenames, key):
    for filename in filenames:
        try:
            with open(filename, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()
                decrypted_data = key.decrypt(encrypted_data)

            decrypted_filename = filename[:-1]  # Usuń ".enc" z nazwy pliku
            with open(decrypted_filename, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)

            print(f"Plik '{filename}' został odszyfrowany jako '{decrypted_filename}'")
        except Exception as e:
            print(f"Błąd przy odszyfrowywaniu pliku '{filename}': {e}")
            decrypt_label.config(text=f"Błąd przy odszyfrowywaniu pliku '{filename}': {e}")

def on_decrypt_files_click():
    global key_file
    if key_file is not None:  # Sprawdzamy, czy klucz jest wczytany (nie jest None)
        key = load_key(key_file)
        if key:
            filenames = filedialog.askopenfilenames(filetypes=[("Pliki do odszyfrowania", "*.x")])
            if filenames:
                decrypt_files(filenames, key)
                decrypt_label.config(text=f"{len(filenames)} plików zostało odszyfrowanych!")
    else:
        decrypt_label.config(text="Błąd: Żaden klucz nie został wczytany. Wczytaj klucz przed próbą odszyfrowywania.")

root = tk.Tk()
root.title("Aplikacja Szyfrowania")

generate_button = tk.Button(root, text="Generuj klucz", width=50, command=on_generate_key_click)
generate_button.pack()

generate_label = tk.Label(root, text="")
generate_label.pack()

load_button = tk.Button(root, text="Wczytaj klucz", width=50, command=on_load_key_click)
load_button.pack()

key_label = tk.Label(root, text="Brak wczytanego klucza")
key_label.pack()

encrypt_button = tk.Button(root, text="Szyfruj pliki", width=50, command=on_encrypt_files_click)
encrypt_button.pack()

encrypt_label = tk.Label(root, text="")
encrypt_label.pack()

decrypt_button = tk.Button(root, text="Odszyfruj pliki", width=50, command=on_decrypt_files_click)
decrypt_button.pack()

decrypt_label = tk.Label(root, text="")
decrypt_label.pack()

root.mainloop()