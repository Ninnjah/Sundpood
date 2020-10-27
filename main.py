import os
import sys
import json
import threading
import soundfile as sf
import sounddevice as sd
from pynput.keyboard import Listener
from PyQt5 import QtWidgets, QtGui, QtCore
import ui_preferences
import ui_sundpood
import ui_overlay
import keys

###! UI !###
class OverlayUi(QtWidgets.QMainWindow, ui_overlay.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            self.hide()
            win.show()

class PreferencesUi(QtWidgets.QMainWindow, ui_preferences.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class MainUi(QtWidgets.QMainWindow, ui_sundpood.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            pref.close()
            self.hide()
            over.show()

    def closeEvent(self, event):
        pref.close()


###! JSON !###
def jsonread(file):                         ## Чтение JSON
    with open(file, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data

def jsonwrite(file, data):                  ## Запись JSON
    with open(file, 'w', encoding='utf-8') as write_file:
        write_file.write(json.dumps(data))


###! FUNCTIONS !###
def find_device(list_):                     # Поиск микшера VoiceMeeter
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't install VoiceMeeter")
    msg.setInformativeText('install VoiceMetter from "redist" folder or download it from \nvb-audio.com/Voicemeeter')
    msg.setWindowTitle('Error')

    index = 0
    device = 'VoiceMeeter Input'
    found = False
    for i in list_:
        if device not in i['name']:
            index += 1
        elif device in i['name']:
            found = True
            break
    if found == False:
        msg.exec_()
        exit()

    return index

def sound_get():                            # Сбор файлов
    def check_format(name, format_):        # Проверка слова до точки с конца строки
        suf = ''
        while name[-1] != '.':
            suf += name[-1]
            name = name[:-1]
        suf = suf[::-1]
        if type(format_) is list:
            if suf in format_:
                return True
            else:
                return False
        elif type(format_) is str:
            if suf == format_:
                return True
            else:
                return False
    
    def sound_convert(path, name, format_): # Конвертация из форматов 'mp3' 'm4a' в format_
        if os.path.exists('ffmpeg.exe'):
            old_name = name
            if check_format(name, ['mp3', 'm4a']):
                while name[-1] != '.':
                    name = name[:-1]
                name += format_

                os.system(f'ffmpeg.exe -i "{os.path.join(path, old_name)}" "{os.path.join(path, name)}"')
                os.remove(f'{os.path.join(path, old_name)}')
            return name
    
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't have any sounds in 'sound' folder")
    msg.setInformativeText('download sound in .wav / .mp3 / .m4a format')
    msg.setWindowTitle('Error')
    
    ffmsg = QtWidgets.QMessageBox()
    ffmsg.setIcon(QtWidgets.QMessageBox.Warning)
    ffmsg.setText("You don't have ffmpeg.exe in the program root folder")
    ffmsg.setInformativeText('download ffmpeg from ffmpeg.org for converting sound files')
    ffmsg.setWindowTitle('Error')

    if os.path.exists('sound'):
        if len(os.listdir('sound')) == 0:
            msg.exec_()

        menu = []
        sounds_list = ['sound\\']
        for i in os.listdir('sound'):
            if os.path.exists('ffmpeg.exe') or not ffmsg:
                if os.path.isfile(os.path.join('sound', i)):
                    name = sound_convert('sound', i, 'wav')
                    if name == None:
                        sounds_list.append(i)
                    else:
                        sounds_list.append(name)
                else:
                    sounds_list_cat = [os.path.join('sound', i)]
                    for x in os.listdir(os.path.join('sound', i)):
                        if os.path.isfile(os.path.join('sound', i, x)):
                            name = sound_convert(os.path.join('sound', i), x, 'wav')
                            if name == None:
                                sounds_list_cat.append(x)
                            else:
                                sounds_list_cat.append(name)
                    menu.append(sounds_list_cat)
            else:
                print('else')
                try:
                    ffmsg.exec_()
                    ffmsg = False
                except AttributeError:
                    pass
        menu.append(sounds_list)

        sounds = []
        for i in os.listdir('sound'):
            if os.path.isfile(os.path.join('sound', i)):
                if check_format(i, 'wav'):
                    sounds.append(i)

        if os.path.exists('settings.json'):
            hotkeys = jsonread('settings.json')['hotkeys']
            KEYS_CMD = jsonread('settings.json')['KEYS_CMD']
            sounds_list = { 'sounds':sounds, 
                            'hotkeys':hotkeys, 
                            'menu':menu,
                            'KEYS_CMD':KEYS_CMD}
        else:
            sounds_list = { 'sounds':sounds, 
                            'hotkeys':{'Push button':''}, 
                            'menu':menu,
                            'KEYS_CMD':{
                            'select_move_up'    :' ',# вверх
                            'select_move_down'  :' ',# вниз
                            'select_move_left'  :' ',# влево
                            'select_move_right' :' ',# вправо
                            'play_sound'        :' ',# Играть
                            'stop_sound'        :' ',# Остановить
                            }}
        for i in COMBOS:
            i.addItems(sounds)

        jsonwrite('settings.json', sounds_list)
    else:
        sounds_list = { 'sounds':'', 
                        'hotkeys':{'Push button':''}, 
                        'menu':'',
                        'KEYS_CMD':{
                            'select_move_up'    :' ',# вверх
                            'select_move_down'  :' ',# вниз
                            'select_move_left'  :' ',# влево
                            'select_move_right' :' ',# вправо
                            'play_sound'        :' ',# Играть
                            'stop_sound'        :' ',# Остановить
                            }}
        jsonwrite('settings.json', sounds_list)
        os.mkdir('sound')
        msg.exec_()

def save():                                 # Сохранение списка хоткеев
    hotkeys = {}
    sounds = jsonread('settings.json')['sounds']
    for i in range(len(COMBOS)):
        hotkeys.setdefault(HOTKEYS[i].text(), COMBOS[i].currentText())

    KEYS_JSON = {}
    for i in KEYS_CMD.keys():
        KEYS_JSON.setdefault(COMMAND_DICT[i], KEYS_CMD[i])

    sounds_list = {'sounds':sounds, 'hotkeys':hotkeys, 'menu':menu, 'KEYS_CMD':KEYS_JSON}
    jsonwrite('settings.json', sounds_list)
    KEYS_JSON = None
    hotkeys = None
    sounds = None

def play_sound(index):                      # Проигрываение звука
    try:
        filename = COMBOS[index].currentText()
        try:
            data, fs = sf.read(os.path.join('sound', filename), dtype='float32')  
            sd.play(data, fs)
        except:
            pass
    except:
        filename = menu[select[0]][select[1]]
        try:
            data, fs = sf.read(os.path.join(menu[select[0]][0], filename), dtype='float32')  
            sd.play(data, fs)
        except:
            pass

def hotkey_remap(btn):                      # Переназначение хоткеев
    def check(key):
        button = HOTKEYS[btn]
        key = str(key).replace("'",'')

        if key not in keys.forbidden:
            HOTKEYS_CMD[HOTKEYS_CMD.index(button.text())] = keys.dict_[key]
            button.setText(keys.dict_[key])
        elif key == 'Key.backspace':
            HOTKEYS_CMD[HOTKEYS_CMD.index(button.text())] = ' '
            button.setText(' ')
        for i in HOTKEYS:
            if i != HOTKEYS[btn]:
                i.setEnabled(True)
        return False

    for i in HOTKEYS:
        if i != HOTKEYS[btn]:
            i.setEnabled(False)

    hotkey_remap_Listener = Listener(
        on_release=check)
    hotkey_remap_Listener.start()

def pref_remap(btn, func_):
    def check(key):
        key = str(key).replace("'",'')
        if key not in keys.forbidden:
            func = find_key(COMMAND_DICT, func_)
            KEYS_CMD.update({func : key})
            btn.setText(keys.dict_[key])
        elif key == 'Key.backspace':
            func = find_key(COMMAND_DICT, func_)
            KEYS_CMD.update({func : ' '})
            btn.setText(' ')
        for i in PREF_BTN:
            i.setEnabled(True)
        return False

    for i in PREF_BTN:
        i.setEnabled(False)

    hotkey_remap_Listener = Listener(
        on_release=check)
    hotkey_remap_Listener.start()

    save()

def find_key(dict, val):
    return next(key for key, value in dict.items() if value == val)


###! CONTROL !###
def select_move(mode):
    select[1] += mode[1]
    select[0] += mode[0]
    if select[0] > len(menu)-1 or select[0] < -len(menu)+1:
        select[0] = 0
    if select[1] > len(menu[select[0]])-1 or select[1] < -len(menu[select[0]])+1:
        select[1] = 0
    if mode[0] != 0:
        select[1] = 0
    over.label.setText(menu[select[0]][select[1]])
    win.select_label.setText(menu[select[0]][select[1]])

def key_check(key):                         # Хоткеи
    key_n = ''
    key = str(key).replace("'",'')
    try:
        key_n = keys.dict_[key]
    except KeyError:
        pass
    print(f'{key_n} in {HOTKEYS_CMD} -- {key_n in HOTKEYS_CMD}')
    if key_n in HOTKEYS_CMD:
        play_sound(HOTKEYS_CMD.index(key_n))
    elif key in KEYS_CMD.values():
        find_key(KEYS_CMD, key)()

def main():                                 # Интерфейс
    win.show()

    key_check_Listener = Listener(
        on_release=key_check)
    key_check_Listener.start()

    
    win.save_button.clicked.connect(save)
    win.actionpreferences.triggered.connect(pref.show)
    win.hotkey_1.clicked.connect(lambda: hotkey_remap(0))
    win.hotkey_2.clicked.connect(lambda: hotkey_remap(1))
    win.hotkey_3.clicked.connect(lambda: hotkey_remap(2))
    win.hotkey_4.clicked.connect(lambda: hotkey_remap(3))
    win.hotkey_5.clicked.connect(lambda: hotkey_remap(4))
    win.hotkey_6.clicked.connect(lambda: hotkey_remap(5))
    win.hotkey_7.clicked.connect(lambda: hotkey_remap(6))
    win.hotkey_8.clicked.connect(lambda: hotkey_remap(7))
    win.hotkey_9.clicked.connect(lambda: hotkey_remap(8))
    win.hotkey_10.clicked.connect(lambda: hotkey_remap(9))
    win.hotkey_11.clicked.connect(lambda: hotkey_remap(10))
    win.hotkey_12.clicked.connect(lambda: hotkey_remap(11))

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


if __name__ == '__main__':
    ### Создание окна ###
    app = QtWidgets.QApplication([])
    over = OverlayUi()
    pref = PreferencesUi()
    win = MainUi()
    COMBOS = [
        win.combo0,
        win.combo1,
        win.combo2,
        win.combo3,
        win.combo4,
        win.combo5,
        win.combo6,
        win.combo7,
        win.combo8,
        win.combo9,
        win.combo10,
        win.combo11,]
    HOTKEYS = [
        win.hotkey_1,
        win.hotkey_2,
        win.hotkey_3,
        win.hotkey_4,
        win.hotkey_5,
        win.hotkey_6,
        win.hotkey_7,
        win.hotkey_8,
        win.hotkey_9,
        win.hotkey_10,
        win.hotkey_11,
        win.hotkey_12,]
    PREF_BTN = [
        pref.select_move_up,
        pref.select_move_down,
        pref.select_move_left,
        pref.select_move_right,
        pref.play_sound,
        pref.stop_sound,]

    ### Поиск устроства ввода ###
    list_ = list(sd.query_devices())
    index = find_device(list_)
    sd.default.device = list_[index]['name']
    sound_get()

    ### Глобальные переменные ###
    sound_get_dict = jsonread('settings.json')
    hotkeys = sound_get_dict['hotkeys']
    menu = sound_get_dict['menu']
    select = [0, 0]
    COMMAND_DICT = {
            lambda: select_move([0, -1]):'select_move_up',      # вверх
            lambda: select_move([0, 1]) :'select_move_down',    # вниз
            lambda: select_move([-1, 0]):'select_move_left',    # влево
            lambda: select_move([1, 0]) :'select_move_right',   # вправо
            lambda: play_sound('')      :'play_sound',          # Играть
            lambda: sd.stop()           :'stop_sound',          # Остановить
    }
    KEYS_CMD = COMMAND_DICT.copy()
    KEYS_JSON = sound_get_dict['KEYS_CMD']
    for i in KEYS_CMD.keys():
        KEYS_CMD.update({i:KEYS_JSON[COMMAND_DICT[i]]})
    KEYS_JSON = None

    combo = 0
    for i in KEYS_CMD.values():
        PREF_BTN[combo].setText(keys.dict_[i])
        combo += 1

    combo = 0
    for i in hotkeys.items():
        index = COMBOS[combo].findText(i[1])
        COMBOS[combo].setCurrentIndex(index)
        HOTKEYS[combo].setText(i[0])
        combo += 1
    combo = None

    HOTKEYS_CMD = [
        HOTKEYS[0].text(),
        HOTKEYS[1].text(),
        HOTKEYS[2].text(),
        HOTKEYS[3].text(),
        HOTKEYS[4].text(),
        HOTKEYS[5].text(),
        HOTKEYS[6].text(),
        HOTKEYS[7].text(),
        HOTKEYS[8].text(),
        HOTKEYS[9].text(),
        HOTKEYS[10].text(),
        HOTKEYS[11].text(),]

    main()
    sys.exit(app.exec())
