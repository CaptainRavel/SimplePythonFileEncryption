import tkinter, os.path, cryptography
from binascii import Error
from cryptography.fernet import Fernet
from cryptography import *
from tkinter import filedialog


root = tkinter.Tk()
root.withdraw()
filetypes = (
    ('All files', '*.*'),
    )

def createKey():
    if os.path.exists('filekey.key'):
        print("""W katalagu programu istnieje już jeden plik klucza! 
Generując kolejny stracisz dostęp do plików zaszyfrowanych nadpisywanym kluczem.
Czy napewno chcesz to zrobić? 
""")
        goodOption = False
        w = input(" Y/N ... ")
        while goodOption == False:
            if w == 'Y' or w == 'y': 
                key = Fernet.generate_key()  
                with open('filekey.key', 'wb') as filekey:                   
                    filekey.write(key) 
                print ('Plik klucza wygenerowany! \n')
                goodOption = True
            elif w == 'N' or w == 'n':
                print('Generowanie nowego klucza anulowane.')
                return
            else:
                w = input("Proszę wcisnąć klawisz 'Y' aby potwierdzić lub 'N' aby anulować operację... ")
    else:
        key = Fernet.generate_key()  
        with open('filekey.key', 'wb') as filekey:                   
            filekey.write(key) 
        print ('Plik klucza wygenerowany! \n')

def encryptText():
    try:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
    except:
        print('Najpierw wygeneruj klucz, lub skopiuj swój do głównego katalogu programu! \n')
        return
    fernet = Fernet(key)
    textToEncrypt = input('\nWpisz tekst do zaszyfrowania:')
    encrypted = str(fernet.encrypt(bytes(textToEncrypt, 'utf-8')), 'utf-8')

    print('\nTekst zaszyfrowany: ')
    print(encrypted)  
    
    
def decryptText():
    try:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
    except:
        print('Najpierw wygeneruj klucz, lub skopiuj swój do głównego katalogu programu! \n')
        return
    fernet = Fernet(key)
    textToDecrypt = input('\nWpisz tekst do odszyfrowania: \n')
    try:
            decrypted = str(fernet.decrypt(bytes(textToDecrypt, 'utf-8')), 'utf-8')
    except (cryptography.fernet.InvalidToken, TypeError, Error):
        print ('Deszyfracja nie powiodła się! Używasz złego klucza, lub podajesz nieprawidłowe dane! \n') 
        return
    print('\nTekst odszyfrowany: ')
    print(decrypted)
         
def encryptFile():     
    try:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
    except:
        print('Najpierw wygeneruj klucz, lub skopiuj swój do głównego katalogu programu! \n')
        return
    fernet = Fernet(key)  
    file = filedialog.askopenfilename(filetypes=filetypes)
    if (len(file) == 0): 
        print('Operacja anulowana. \n')
        return
    with open(file, 'rb') as file:
        original = file.read()      
    encrypted = fernet.encrypt(original)  
    file = filedialog.asksaveasfilename(filetypes=filetypes)
    if (len(file) == 0): 
        print('Operacja anulowana. \n')
        return
    with open(file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print('Zapisano zaszyfrowany plik: ' + str(file) + '\n')
    
    
def decryptFile():  
    try:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
    except:
        print('Najpierw wygeneruj klucz, lub skopiuj swój do głównego katalogu programu! \n')
        return
    fernet = Fernet(key)  
    file = filedialog.askopenfilename(filetypes=filetypes)
    if (len(file) == 0): 
        print('Operacja anulowana. \n')
        return
    with open(file, 'rb') as enc_file:
        encrypted = enc_file.read()  
    try:
        decrypted = fernet.decrypt(encrypted) 
    except (cryptography.fernet.InvalidToken, TypeError, Error):
        print ('Deszyfracja nie powiodła się! Używasz innego klucza! \n') 
        return
    file = filedialog.asksaveasfilename(filetypes=filetypes)
    if (len(file) == 0): 
        print('Operacja anulowana. \n')
        return
    with open(file, 'wb') as dec_file:
        dec_file.write(decrypted)
    print('Zapisano odszyfrowany plik: ' + str(file) + '\n')


print("""Witaj, dzięki temu programowi zaszyfrujesz swoje wiadomości i pliki.
Po wybraniu odpowiedniej opcji wybierz plik do szyfrowania i odszyfrowania i zapisz rezultat w nowym pliku.

UWAGA!
Do prawdłowego szyfrowania potrzebujesz pliku klucza, jeśli go nie masz, wystarczy że wygenerujesz nowy.
Jeśli jednak już go posiadasz, umieść go w głównym katalogu programu.
Plik klucza powinien nazywać się filekey.key!

By wyświetlić listę dostępnych czynności wpisz: help


Wpisz numer czynności którą chcesz wykonać: 
1. Wygeneruj plik z kluczem
2. Zaszyfruj wpisany tekst
3. Odszyfruj wpisany tekst
4. Zaszyfruj wybrany plik
5. Odszyfruj wybrany plik
6. Zamknij program
""")

wybor = input(" \nPodaj numer operacji: ")

while True:
    if wybor == '1':
        createKey()
        wybor = None
        wybor = input(" \nPodaj numer operacji: ")
    elif wybor == '2':
        encryptText()
        wybor = None
        wybor = input(" \nPodaj numer operacji: ")
    elif wybor == '3':
        decryptText()
        wybor = None
        wybor = input(" \nPodaj numer operacji: ")
    elif wybor == '4':
        encryptFile()
        wybor = None
        wybor = input(" \nPodaj numer operacji: ")
    elif wybor == '5':
        decryptFile()
        wybor = None
        wybor = input(" \nPodaj numer operacji: ")
    elif wybor == '6':
        exit()
    elif wybor == 'help':
        print("""Czynności jakie możesz wykonać: 
1. Wygeneruj plik z kluczem
2. Zaszyfruj wpisany tekst
3. Odszyfruj wpisany tekst
4. Zaszyfruj wybrany plik
5. Odszyfruj wybrany plik
6. Zamknij program""")
        wybor == None
        wybor = input(" \nPodaj numer operacji: ")
    else: 
        wybor = None 
        wybor = input("\nPodaj prawidłowy numer operacji: ")




  

 
