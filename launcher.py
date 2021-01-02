import os
from cryptography.fernet import Fernet
import key

### Добавь здесь модули нужные твоей программе ###
import pygame
import sounddevice as sd
from pynput.keyboard import Listener
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from data import ui_preferences
from data import ui_hotkeys
from data import ui_sundpood
from data import ui_overlay
from data import keys
import themes
### ^^^                                    ^^^ ###

def decrypt(filename, key):
    # Расшифруем файл и записываем его
    f = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
        
    decrypted_data = f.decrypt(encrypted_data)
    
    return decrypted_data.decode('utf-8')

exec(decrypt(os.path.join('data', 'sundpood-runtime.sr') , key.KEY))
