import os
import tkinter as tk
from cryptography.fernet import Fernet
from tkinter import filedialog

key_loaded = None
key_file = None


def generate_key(filename):
    key = Fernet.generate_key()
    with open(filename, 'wb') as filekey:
        filekey.write(key)
        print(f"Plik klucza '{filename}' został wygenerowany!")


def on_generate_key_click():
    initial_dir = os.getcwd()  # Pobierz aktualny katalog roboczy
    filename = filedialog.asksaveasfilename(initialdir=initial_dir, defaultextension=".key",
                                            filetypes=[("Klucz szyfrowania", "*.key")])
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
    initial_dir = os.getcwd()  # Pobierz aktualny katalog roboczy
    filename = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Klucz szyfrowania", "*.key")])
    if filename:
        global key_loaded
        global key_file
        loaded_key = load_key(filename)
        key_file = filename
        if loaded_key:
            key_label.config(text=f"Wczytano klucz: {filename}")
            key_loaded = True
        else:
            key_label.config(text="Błąd przy wczytywaniu klucza.")
            key_loaded = False


def create_encryption_folder(local_key_file):
    key_folder = os.path.splitext(os.path.basename(local_key_file))[0] + " encrypted files"
    if not os.path.exists(key_folder):
        os.mkdir(key_folder)
    return key_folder


def encrypt_files(filenames, local_key_file):
    key_folder = create_encryption_folder(local_key_file)
    key = load_key(local_key_file)

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


def on_encrypt_files_click():
    global key_file
    if key_file is not None:
        filenames = filedialog.askopenfilenames(filetypes=[("Pliki do zaszyfrowania", "*.*")])
        if filenames:
            key_folder = create_encryption_folder(key_file)
            encrypt_files(filenames, key_file)
            encrypt_label.config(text=f"{len(filenames)} plików zostało zaszyfrowanych w folderze '{key_folder}'")
    else:
        encrypt_label.config(text="Błąd: Żaden klucz nie został wczytany. Wczytaj klucz przed próbą szyfrowania.")


def create_decryption_folder(local_key_file):
    key_folder = os.path.splitext(os.path.basename(local_key_file))[0] + " decrypted files"
    if not os.path.exists(key_folder):
        os.mkdir(key_folder)
    return key_folder


def decrypt_files(filenames, local_key_file):
    key_folder = create_decryption_folder(local_key_file)
    key = load_key(local_key_file)
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
        decrypt_label.config(
            text="Błąd: Wystąpiły problemy podczas odszyfrowywania niektórych plików."
                 "Upewnij się, że używasz odpowiedniego klucza!")
    else:
        decrypt_label.config(text=f"{decrypted_count} plików zostało odszyfrowanych w folderze '{key_folder}'")


def on_decrypt_files_click():
    global key_file
    if key_file is not None:
        filenames = filedialog.askopenfilenames(filetypes=[("Pliki do odszyfrowania", "*.x")])
        if filenames:
            decrypt_files(filenames, key_file)
    else:
        decrypt_label.config(text="Błąd: Żaden klucz nie został wczytany. Wczytaj klucz przed próbą odszyfrowywania.")


root = tk.Tk()
root.title("Aplikacja Szyfrowania")
root.geometry("650x200")
root.update_idletasks()
root.minsize(650, 200)  # Ustawia minimalny rozmiar na 650 × 200 pikseli

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
