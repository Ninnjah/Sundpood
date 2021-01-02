#\ SundPood version 0201 /#

import os
import sys
import json
from time import time
import pygame as pg
import sounddevice as sd
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from data import ui_preferences
from data import ui_hotkeys
from data import ui_sundpood
from data import ui_overlay
from data import keys
import themes
import key


###! UI !###
class OverlayUi(QtWidgets.QMainWindow, ui_overlay.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(QtCore.QRect(0, 0, 250, 20))
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            self.hide()
            win.show()

class PreferencesUi(QtWidgets.QMainWindow, ui_preferences.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)
    
    def closeEvent(self, event):
        save()

class HotkeysUi(QtWidgets.QMainWindow, ui_hotkeys.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

class MainUi(QtWidgets.QMainWindow, ui_sundpood.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.volume_slider.valueChanged[int].connect(change_volume)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x-x_w, y-y_w)
        except AttributeError:
            pass
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            pref.close()
            self.hide()
            over.show()

    def closeEvent(self, event):
        save()
        if os.path.exists('.play'):
            os.remove('.play')
        hotk.close()
        pref.close()


###! JSON !###
def jsonread(file):
    '''
    Чтение JSON файла file
    file - имя JSON файла, может содержать полный или относительный путь
    '''
    with open(file, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data

def jsonwrite(file, data):
    '''
    Запись в JSON файл file данные data
    file - имя JSON файла, может содержать полный или относительный путь
    data - данные, может быть словарем/списком/кортежем/строкой/числом
    '''
    with open(file, 'w', encoding='utf-8') as write_file:
        write_file.write(json.dumps(data))


###! FUNCTIONS !###
def toggle_stylesheet(path):
    '''
    Toggle the stylesheet to use the desired path in the Qt resource
    system (prefixed by `:/`) or generically (a path to a file on
    system).

    :path:      A full path to a resource or file on system
    '''

    # get the QApplication instance,  or crash if not set
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("No Qt Application found.")

    path = os.path.join('themes', path)
    file = QFile(path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    theme = stream.readAll()

    pref.setStyleSheet(theme)
    win.setStyleSheet(theme)
    hotk.setStyleSheet(theme)

def find_device():
    '''
    Ищем устройство device и возвращаем его индекс
    '''

    list_ = list(sd.query_devices())    # Список устройств вывода звука
    device = ["CABLE Input (VB-Audio Virtual Cable)", 
            "VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)"]# Имя искомого устройства

    msg = QtWidgets.QMessageBox()       # Окно ошибки (Устройство не найдено)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't install VoiceMeeter")
    msg.setInformativeText('install VoiceMetter from "redist" folder or download it from \nvb-audio.com/Voicemeeter')
    msg.setWindowTitle('Error')

    for i in list_:
        for d in device:
            if d in i['name']:
                return i['name']
    
    msg.exec_()
    exit()

def get_files(dir_, config):
    '''
    Сбор всех аудифайлов
    dir_ - Путь к папке со звуками
    config - Имя файла настроек
    '''
    msg = QtWidgets.QMessageBox()       # Окно ошибки (Не найдены файлы в папке 'sound')
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't have any sounds in 'sound' folder")
    msg.setInformativeText('download sound in .wav / .mp3 / .m4a format')
    msg.setWindowTitle('Error')

    if os.path.exists(dir_):
        if len(os.listdir(dir_)) == 0:
            msg.exec_()

        sounds = []                     # Все аудио файлы
        sounds_list = [f'{dir_}\\']       # Начальная категория

        for i in os.listdir(dir_):
            if os.path.isfile(os.path.join(dir_, i)):
                name = os.path.join(dir_, i)
                if name == None:
                    sounds_list.append(i)
                elif os.path.splitext(i)[1] in ['.mp3', '.m4a', '.wav']:
                    sounds_list.append(i)
            else:
                sounds_list_cat = [os.path.join(dir_, i)]
                for x in os.listdir(os.path.join(dir_, i)):
                    if os.path.isfile(os.path.join(dir_, i, x)):
                        if name == None:
                            sounds_list_cat.append(x)
                        elif os.path.splitext(x)[1] in ['.mp3', '.m4a', '.wav']:
                            sounds_list_cat.append(x)
                sounds.append(sounds_list_cat)
        sounds.append(sounds_list)

        if os.path.exists(config):
            hotkeys = jsonread(config)['hotkeys']
            theme = jsonread(config)['Theme']
            KEYS_CMD = jsonread(config)['KEYS_CMD']
            sounds_list = { 'hotkeys':hotkeys, 
                            'sounds':sounds,
                            'Theme':theme,
                            'KEYS_CMD':KEYS_CMD}
        else:
            sounds_list = { 'hotkeys':{}, 
                            'sounds':sounds,
                            'Theme':'None',
                            'KEYS_CMD':{
                            'select_move_up'    :' ',# вверх
                            'select_move_down'  :' ',# вниз
                            'select_move_left'  :' ',# влево
                            'select_move_right' :' ',# вправо
                            'play_sound'        :' ',# Играть
                            'stop_sound'        :' ',# Остановить
                            }}

        jsonwrite(config, sounds_list)
    else:
        sounds_list = { 'hotkeys':{}, 
                        'sounds':'',
                        'Theme':'None',
                        'KEYS_CMD':{
                            'select_move_up'    :' ',# вверх
                            'select_move_down'  :' ',# вниз
                            'select_move_left'  :' ',# влево
                            'select_move_right' :' ',# вправо
                            'play_sound'        :' ',# Играть
                            'stop_sound'        :' ',# Остановить
                            }}
        jsonwrite(config, sounds_list)
        os.mkdir(dir_)
        msg.exec_()

def change_volume(value):
    pg.mixer.music.set_volume(value/100)

def play_sound(*argv):
    if False in argv:
        try:
            sound = os.path.join(win.soundList.item(0).text(),
                    win.soundList.currentItem().text())
        except AttributeError:
            return False
    else:
        sound = argv[0]
    try:
        pg.mixer.music.load(sound)
        pg.mixer.music.play()
        pg.event.wait()
    except RuntimeError:
        pass

def cat_select(cat):
    win.soundList.clear()
    for i in menu:
        if 'sound' + cat == i[0]:
            win.soundList.addItems(i)

def hotkey_remap():
    '''
    Переназначение хоткея
    btn - индекс кнопки хоткея в списке HOTKEYS
    '''
    def check(key):
        key = str(key).replace("'",'')
        try:
            sound = os.path.join(win.soundList.item(0).text(),
                        win.soundList.currentItem().text())
        except AttributeError:
            win.hkset.setEnabled(True)
            return False

        if key not in keys.forbidden:
            hotkeys.update({key:sound})
        elif key == 'Key.backspace':
            del hotkeys[find_key(hotkeys, sound)]

        save()
        hotk.hotkeyList.clear()
        for i in sound_get_dict['sounds']:
            for x in i:
                x = os.path.join(i[0], x)
                if x in hotkeys.values():
                    hotk.hotkeyList.addItem(f'{find_key(hotkeys, x)}\t:{x}')

        win.hkset.setEnabled(True)
        return False

    win.hkset.setEnabled(False)

    hotkey_remap_Listener = Listener(
        on_release=check)
    hotkey_remap_Listener.start()

def hotkey_delete():
    key = hotk.hotkeyList.currentItem().text().split(':')[0].replace('\t', '')
    hotkeys.pop(key)

    save()
    hotk.hotkeyList.clear()
    for i in sound_get_dict['sounds']:
        for x in i:
            x = os.path.join(i[0], x)
            if x in hotkeys.values():
                hotk.hotkeyList.addItem(f'{find_key(hotkeys, x)}\t:{x}')

def pref_remap(btn, func_):
    '''
    Переназначение клавиши в окно Preference
    btn - PyQt5 кнопка
    func_ - строковое значени функции из словаря KEYS_CMD
    '''
    def check(key):
        '''
        Проверка кнопки btn на не участие 
            в списке запрещенных клавиш keys.forbidden
            если это клавиша 'Key.backspace' то стираем значение
        key - pynput код клавиши
        '''
        key = str(key).replace("'",'')
        if key not in keys.forbidden:
            KEYS_CMD.update({find_key(COMMAND_DICT, func_) : key})
            btn.setText(keys.dict_[key])
        elif key == 'Key.backspace':
            KEYS_CMD.update({find_key(COMMAND_DICT, func_) : ' '})
            btn.setText(' ')
        for i in PREF_BTN:
            i.setEnabled(True)
        save()
        return False

    for i in PREF_BTN:
        i.setEnabled(False)

    hotkey_remap_Listener = Listener(
        on_release=check)
    hotkey_remap_Listener.start()

def find_key(dict, val):
    '''
    Поиск ключа в словаре dict по значению val
    dict - словарь
    val - значение
    '''
    return next((key for key, value in dict.items() if value == val), None)

def check_update():
    def decrypt(filename, key):
        f = Fernet(key)
        with open(filename, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = f.decrypt(encrypted_data)

        return decrypted_data.decode('utf-8')

    file_ = decrypt(os.path.join('data', 'sundpood-runtime.sr') , key.KEY)
    version = ''
    for i in file_:
        if i != '/':
            version += i
        else:
            break
    print(VERSION)
    return version.split(' ')[3]

def save():
    '''
    Сохранение настроек оверлея и глобальных хоткеев
    '''
    sounds = jsonread(config)['sounds']# Все аудиофайлы
    
    KEYS_JSON = {}                      # Настроенные клавиши
    for i in KEYS_CMD.keys():
        KEYS_JSON.setdefault(COMMAND_DICT[i], KEYS_CMD[i])

    try:
        theme = pref.themesList.currentItem().text()
    except AttributeError:
        theme = jsonread(config)['Theme']
    
    sounds_list = {'sounds':sounds, 'hotkeys':hotkeys, 'Theme':theme, 'KEYS_CMD':KEYS_JSON}
    jsonwrite(config, sounds_list)

###! CONTROL !###
def select_move(mode):
    '''
    Перемешение по оверлейному меню
    mode - кортеж из двух цифр 
        (смещение по категории, смещение по списку)
    '''
    select[0] += mode[0]    # Категории
    select[1] += mode[1]    # Файлы в категории
    if select[0] > len(menu)-1 or select[0] < -len(menu)+1:
        select[0] = 0
    if select[1] > len(menu[select[0]])-1 or select[1] < -len(menu[select[0]])+1:
        select[1] = 0
    if mode[0] != 0:
        select[1] = 0
    over.label.setText(menu[select[0]][select[1]])
    win.select_label.setText(menu[select[0]][select[1]])

def key_check(key):
    key = str(key).replace("'",'')  # Преобразование кода в строку
    key_n = ''                      # Переведенное значение клавиши
    try:
        key_n = keys.dict_[key]
    except KeyError:
        pass
    if key in hotkeys.keys():
        play_sound(hotkeys[key])
    elif key in KEYS_CMD.values():
        find_key(KEYS_CMD, key)()

def main():
    key_check_Listener = Listener(
        on_release=key_check)
    key_check_Listener.start()

    win.exit_button.clicked.connect(win.close)
    win.min_button.clicked.connect(win.showMinimized)
    pref.exit_button.clicked.connect(pref.close)
    pref.min_button.clicked.connect(pref.showMinimized)
    hotk.exit_button.clicked.connect(hotk.close)
    hotk.min_button.clicked.connect(hotk.showMinimized)

    win.hkset.clicked.connect(hotkey_remap)
    win.pref_button.clicked.connect(pref.show)
    win.hotkeys_button.clicked.connect(hotk.show)
    win.catList.currentTextChanged.connect(cat_select)
    win.stop_button.clicked.connect(lambda: sd.stop())
    win.play_button.clicked.connect(play_sound)

    pref.play_sound.clicked.connect(
        lambda: pref_remap(pref.play_sound, 'play_sound'))
    pref.stop_sound.clicked.connect(
        lambda: pref_remap(pref.stop_sound, 'stop_sound'))
    pref.select_move_up.clicked.connect(
        lambda: pref_remap(pref.select_move_up, 'select_move_up'))
    pref.select_move_down.clicked.connect(
        lambda: pref_remap(pref.select_move_down, 'select_move_down'))
    pref.select_move_left.clicked.connect(
        lambda: pref_remap(pref.select_move_left, 'select_move_left'))
    pref.select_move_right.clicked.connect(
        lambda: pref_remap(pref.select_move_right, 'select_move_right'))
    pref.themesList.currentTextChanged.connect(toggle_stylesheet)
    pref.update_button.clicked.connect(check_update)

    hotk.delete_button.clicked.connect(hotkey_delete)

    win.show()


if __name__ == '__main__':
    ### Создание окна ###
    app = QApplication([])              # Приложение
    over = OverlayUi()                  # Окно оверлея
    pref = PreferencesUi()              # Окно настроек
    hotk = HotkeysUi()                  # Окно хоткеев
    win = MainUi()                      # Основное окно

    PREF_BTN = [                        # Список кнопок настроек клавиш в pref
        pref.select_move_up,
        pref.select_move_down,
        pref.select_move_left,
        pref.select_move_right,
        pref.play_sound,
        pref.stop_sound,]
    
    ### Поиск устроства ввода ###
    pg.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pg.mixer.init(devicename=find_device()) # Установка устройства вывода по умолчанию
    
    ### Глобальные переменные ###
    VERSION = 102
    dir_ = 'sound'
    config = 'settings.json'
    get_files(dir_, config)             # Сбор всех аудиофайлов
    sound_get_dict = jsonread(config)   # Загрузка данных
    hotkeys = sound_get_dict['hotkeys'] # Загрузка словаря хоткеев
    theme = sound_get_dict['Theme']     # Загрузка темы
    menu = sound_get_dict['sounds']     # Загрузка оверлейного меню
    select = [0, 0]                     # Установка курсора оверлея в нулевую позицию

    if theme != 'None':
        toggle_stylesheet(theme)
    pref.themesList.addItems(os.listdir('themes'))

    for i in sound_get_dict['sounds']:
        win.catList.addItem(i[0].replace('sound', ''))

        for x in i:
            x = os.path.join(i[0], x)
            if x in hotkeys.values():
                hotk.hotkeyList.addItem(f'{find_key(hotkeys, x)}\t: {x}')

    
    COMMAND_DICT = {                    # Словарь функций к строковому значению
            lambda: select_move((0, -1)):'select_move_up',      # вверх
            lambda: select_move((0, 1)) :'select_move_down',    # вниз
            lambda: select_move((-1, 0)):'select_move_left',    # влево
            lambda: select_move((1, 0)) :'select_move_right',   # вправо
            lambda: play_sound(os.path.join(menu[select[0]][0], 
                menu[select[0]][select[1]])):'play_sound',      # Играть
            lambda: sd.stop()           :'stop_sound',          # Остановить
    }
    KEYS_JSON = sound_get_dict['KEYS_CMD']# Загрузка настроенных клавиш
    KEYS_CMD = COMMAND_DICT.copy()      # Настроенные клавиши

    ### Установка настроенных клавиш ###
    for i in KEYS_CMD.keys():           
        KEYS_CMD.update({i:KEYS_JSON[COMMAND_DICT[i]]})
    KEYS_JSON = None

    combo = 0
    for i in KEYS_CMD.values():
        PREF_BTN[combo].setText(keys.dict_[i])
        combo += 1

    main()

    sys.exit(app.exec())