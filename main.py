import os
import sys
import json
import threading
import keyboard
import soundfile as sf
import sounddevice as sd
from PyQt5 import QtWidgets, QtGui, QtCore
import ui_sundpood
import ui_overlay

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

    if os.path.exists('settings.json') and mode == False:
        sounds_list = jsonread('settings.json')
    
    elif not os.path.exists('settings.json') or mode == True:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("You don't have any sounds in 'sound' folder")
        msg.setInformativeText('download sound in .wav / .mp3 / .m4a format')
        msg.setWindowTitle('Error')
        
        if os.path.exists('sound'):
            sounds = []
            for i in os.listdir('sound'):
                format_ = ''
                name = i
                if os.path.isfile(os.path.join('sound', i)):
                    while i[-1] != '.':
                        format_ += i[-1]
                        i = i[:-1]
                    format_ = format_[::-1]
                    if format_ == 'wav':
                        sounds.append(name)

            if len(sounds) == 0:
                msg.exec_()
                exit()

            menu = []
            sounds_list = ['sound\\']
            for i in os.listdir('sound'):                # Коонвертируем файлы в .wav
                name = i
                format_ = ''
                if os.path.isfile(os.path.join('sound', i)):
                    while i[-1] != '.':
                        format_ += i[-1]
                        i = i[:-1]
                    format_ = format_[::-1]
                    if format_ in ['mp3', 'm4a']:
                        os.system(f'ffmpeg.exe -i "sound\\{name}" "sound\\{i}wav"')
                        os.remove(f'sound\\{name}')
                    sounds_list.append(name)
                else:
                    sounds_list_cat = [os.path.join('sound', i)]
                    for x in os.listdir(os.path.join('sound', i)):                # Коонвертируем файлы в .wav
                        name = x
                        format_ = ''
                        if os.path.isfile(os.path.join('sound', i, x)):
                            while x[-1] != '.':
                                format_ += x[-1]
                                x = x[:-1]
                            format_ = format_[::-1]
                            if format_ in ['mp3', 'm4a']:
                                os.system(f'ffmpeg.exe -i "sound\\{os.path.join(i, name)}" "sound\\{os.path.join(i, x)}wav"')
                                os.remove(f'sound\\{os.path.join(i, name)}')
                            sounds_list_cat.append(name)
                    menu.append(sounds_list_cat)
            menu.append(sounds_list)

            if os.path.exists('settings.json'):
                hotkeys = jsonread('settings.json')['hotkeys']
                sounds_list = {'sounds':sounds, 'hotkeys':hotkeys, 'menu':menu}
            else:
                sounds_list = {'sounds':sounds, 'hotkeys':{'':''}, 'menu':menu}

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
        print(COMBOS[i].currentText())
        hotkeys.setdefault(HOTKEYS[i].text(), COMBOS[i].currentText())
        print(hotkeys)

    sounds_list = {'sounds':sounds, 'hotkeys':hotkeys, 'menu':menu}
    jsonwrite('settings.json', sounds_list)
    sounds = None
    hotkeys = None

def play_sound(index):                      # Проигрываение звука
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

def hotkey_remap(btn):
    button = HOTKEYS[btn]
    key = keyboard.read_key()
    if key not in ['esc']:
        print(key)
        print(COMMANDS[COMMANDS.index(button.text())])
        COMMANDS[COMMANDS.index(button.text())] = key
        button.setText(key)

###! CONTROL !###
def key(arg):                               # Хоткеи
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

    keyboard.add_hotkey(72, select_move, args=[[0, -1]])
    keyboard.add_hotkey(80, select_move, args=[[0, 1]])
    keyboard.add_hotkey(77, select_move, args=[[1, 0]])
    keyboard.add_hotkey(75, select_move, args=[[-1, 0]])
    keyboard.add_hotkey(76, play_sound, args=[''])
    keyboard.add_hotkey(73, sd.stop)

    while True:
        key = keyboard.read_key()
        print(keyboard.key_to_scan_codes(key))
        if key == 'esc':
            break
        elif key in COMMANDS:
            print(key)
            play_sound(COMMANDS.index(key))


def main():                                 # Интерфейс

    hotkeys_thread.start()
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
    win.show()

    select = [0, 0]
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
    
    sounds = sound_get(True)['hotkeys']
    combo = 0
    for i in sounds.items():
        index = COMBOS[combo].findText(i[1])
        COMBOS[combo].setCurrentIndex(index)
        HOTKEYS[combo].setText(i[0])
        combo += 1

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
    
    menu = sound_get(True)['menu']

    hotkeys_thread = threading.Thread(target=key, args=(1,))
    hotkeys_thread.setDaemon(True)
    
    main()
    sys.exit(app.exec())
