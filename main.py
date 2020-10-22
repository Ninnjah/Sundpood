import os
import sys
import json
import threading
import keyboard
from pynput.keyboard import Listener
import soundfile as sf
import sounddevice as sd
from PyQt5 import QtWidgets, QtGui, QtCore
import ui_sundpood
import ui_overlay
import keys

class OverlayUi(QtWidgets.QMainWindow, ui_overlay.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            self.hide()
            win.show()

class MainUi(QtWidgets.QMainWindow, ui_sundpood.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            self.hide()
            over.show()


###! JSON !###
def jsonread(file):                         ## Чтение JSON
    with open(file, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data

def jsonwrite(file, data):                  ## Запись JSON
    with open(file, 'w', encoding='utf-8') as write_file:
        write_file.write(json.dumps(data))


###! FUNCTIONS !###
def found_device(list_):                    # Поиск микшера VoiceMeeter
    index = 0
    for i in list_:
        if 'VoiceMeeter Input' in i['name']:
            break
        index += 1
    return index

def sound_get(mode):                        # Сбор файлов
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
        old_name = name
        if check_format(name, ['mp3', 'm4a']):
            while name[-1] != '.':
                name = name[:-1]
            name += format_

            os.system(f'''ffmpeg.exe -i "{os.path.join(path, old_name)}" 
                        "{os.path.join(path, name)}"''')
            os.remove(f'{os.path.join(path, old_name)}')
        return name
    
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't have any sounds in 'sound' folder")
    msg.setInformativeText('download sound in .wav / .mp3 / .m4a format')
    msg.setWindowTitle('Error')
    
    if os.path.exists('settings.json') and mode == False:
        sounds_list = jsonread('settings.json')
    
    elif not os.path.exists('settings.json') or mode == True:
        if os.path.exists('sound'):
            if len(os.listdir('sound')) == 0:
                msg.exec_()
                exit()

            menu = []
            sounds_list = ['sound\\']
            for i in os.listdir('sound'):
                if os.path.isfile(os.path.join('sound', i)):
                    i = sound_convert('sound', i, 'wav')
                    sounds_list.append(i)
                else:
                    sounds_list_cat = [os.path.join('sound', i)]
                    for x in os.listdir(os.path.join('sound', i)):
                        if os.path.isfile(os.path.join('sound', i, x)):
                            x = sound_convert(os.path.join('sound', i), x, 'wav')
                            sounds_list_cat.append(x)
                    menu.append(sounds_list_cat)
            menu.append(sounds_list)

            sounds = []
            for i in os.listdir('sound'):
                if os.path.isfile(os.path.join('sound', i)):
                    if check_format(i, 'wav'):
                        sounds.append(i)

            if os.path.exists('settings.json'):
                hotkeys = jsonread('settings.json')['hotkeys']
                sounds_list = {'sound':sounds, 
                                'hotkeys':hotkeys, 
                                'menu':menu}
            else:
                sounds_list = {'sounds':sounds, 
                                'hotkeys':{'Push button':''}, 
                                'menu':menu}

            for i in COMBOS:
                i.addItems(sounds)
            jsonwrite('settings.json', sounds_list)
        else:
            msg.exec_()
            exit()
    return sounds_list

def save():                                 # Сохранение списка хоткеев
    hotkeys = {}
    sounds = sound_get(False)
    for i in range(len(COMBOS)):
        hotkeys.setdefault(HOTKEYS[i].text(), COMBOS[i].currentText())

    sounds_list = {'sounds':sounds, 'hotkeys':hotkeys, 'menu':menu}
    jsonwrite('settings.json', sounds_list)
    sounds = None
    hotkeys = None

def play_sound(index):                      # Проигрываение звука
    print(index)
    try:
        filename = COMBOS[index].currentText()
        try:
            data, fs = sf.read(os.path.join('sound', filename), dtype='float32')  
            sd.play(data, fs)
            keyboard.wait(sd.play())
            sd.wait()
        except:
            pass
    except:
        filename = menu[select[0]][select[1]]
        try:
            data, fs = sf.read(os.path.join(menu[select[0]][0], filename), dtype='float32')  
            sd.play(data, fs)
            keyboard.wait(sd.play())
            sd.wait()
        except:
            pass

def hotkey_remap(btn):                      # Переназначение хоткеев
    def check(key):
        button = HOTKEYS[btn]
        key = str(key)
        if key not in keys.forbidden:
            print(key)
            COMMANDS[COMMANDS.index(button.text())] = key.replace("'",'')
            button.setText(key.replace("'",''))
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


###! CONTROL !###
def key_check(key):                         # Хоткеи
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
    
    key = str(key)
    if key.replace("'",'') in COMMANDS:
        play_sound(COMMANDS.index(key.replace("'",'')))

    keyboard.add_hotkey(72, select_move, args=[[0, -1]])
    keyboard.add_hotkey(80, select_move, args=[[0, 1]])
    keyboard.add_hotkey(77, select_move, args=[[1, 0]])
    keyboard.add_hotkey(75, select_move, args=[[-1, 0]])
    keyboard.add_hotkey(76, play_sound, args=[''])
    keyboard.add_hotkey(73, sd.stop)

def main():                                 # Интерфейс
    win.show()
    key_check_Listener.start()

    win.save_button.clicked.connect(save)
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


if __name__ == '__main__':
    ### Поиск устроства ввода ###
    list_ = list(sd.query_devices())
    index = found_device(list_)
    sd.default.device = list_[index]['name']

    ### Создание окна ###
    app = QtWidgets.QApplication([])
    over = OverlayUi()
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
    
    sound_get_dict = sound_get(True)

    ### Глобальные переменные ###
    sounds = sound_get_dict['hotkeys']
    menu = sound_get_dict['menu']
    select = [0, 0]
    combo = 0
    for i in sounds.items():
        index = COMBOS[combo].findText(i[1])
        COMBOS[combo].setCurrentIndex(index)
        HOTKEYS[combo].setText(i[0])
        combo += 1
    combo = None

    COMMANDS = [
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
    
    key_check_Listener = Listener(
        on_release=key_check)

    main()
    sys.exit(app.exec())
