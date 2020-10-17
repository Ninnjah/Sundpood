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

def sound_get(mode):              # Сбор файлов
    MUSIC = ['Music']
    MEME = ['Meme']
    OTHER = ['Other']
    CATS = [MUSIC, MEME, OTHER]

    if os.path.exists('settings.json') and mode == False:
        sounds_list = jsonread('settings.json')
    
    elif not os.path.exists('settings.json') or mode == True:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("You don't have any sounds in 'sound' folder")
        msg.setInformativeText('download sound in .wav / .mp3 / .m4a format')
        msg.setWindowTitle('Error')
        
        if os.path.exists('sound'):
            sounds = os.listdir('sound')

            if len(sounds) == 0:
                msg.exec_()
                exit()

            for i in os.listdir('sound'):                # Коонвертируем файлы в .wav
                name = i
                format_ = ''
                while i[-1] != '.':
                    format_ += i[-1]
                    i = i[:-1]
                format_ = format_[::-1]
                if format_ in ['mp3', 'm4a']:
                    os.system(f'ffmpeg.exe -i "sound\\{name}" "sound\\{i}wav"')
                    os.remove(f'sound\\{name}')
            
            sounds = os.listdir('sound')
            for i in sounds:                # Ищем ключевые слова в названиях песен
                tag = ''
                for x in i:
                    if x not in [' ', '.', '-', '_']:
                        tag += x
                    else:
                        break
                if tag.lower() == 'music':
                    MUSIC.append(i)
                elif tag.lower() == 'meme':
                    MEME.append(i)
                else:
                    OTHER.append(i)
            
            menu = []
            for i in CATS:
                menu.append(i)

            if os.path.exists('settings.json'):
                hotkeys = jsonread('settings.json')[1]
                sounds_list = [sounds, hotkeys, menu]
            else:
                sounds_list = [sounds, ['', '', '', '', '', '', '', '', '', '', '', ''], menu]

            for i in COMBOS:
                i.addItems(sounds)
            jsonwrite('settings.json', sounds_list)
        else:
            msg.exec_()
            exit()
    return sounds_list

def save():                                 # Сохранение списка хоткеев
    hotkeys = []
    sounds = sound_get(False)
    for i in COMBOS:
        hotkeys.append(i.currentText())
    jsonwrite('settings.json', [sounds, hotkeys])
    sounds = None
    hotkeys = None

def play_sound(index):                      # Проигрываение звука
    try:
        filename = COMBOS[index].currentText()
    except:
        filename = index
    try:
        data, fs = sf.read(os.path.join('sound', filename), dtype='float32')  
        sd.play(data, fs)
        keyboard.wait(sd.play())
        sd.wait()
    except:
        pass


###! CONTROL !###
def key(arg):                               # Хоткеи
    
    select = [0, 0]
    
    def select_move(mode):
        select[1] += mode[1]
        select[0] += mode[0]
        if select[0] > len(menu)-1 or select[0] < -len(menu)+1:
            select[0] = 0
        if select[1] > len(menu[select[0]])-1 or select[1] < -len(menu[select[0]])+1:
            select[1] = 0
        if mode[0] > 0:
            select[1] = 0
        over.label.setText(menu[select[0]][select[1]])
        win.select_label.setText(menu[select[0]][select[1]])

    keyboard.add_hotkey('f1', play_sound, args=[0])
    keyboard.add_hotkey('f2', play_sound, args=[1])
    keyboard.add_hotkey('f3', play_sound, args=[2])
    keyboard.add_hotkey('f4', play_sound, args=[3])
    keyboard.add_hotkey('f5', play_sound, args=[4])
    keyboard.add_hotkey('f6', play_sound, args=[5])
    keyboard.add_hotkey('f7', play_sound, args=[6])
    keyboard.add_hotkey('f8', play_sound, args=[7])
    keyboard.add_hotkey('f9', play_sound, args=[8])
    keyboard.add_hotkey('f10', play_sound, args=[9])
    keyboard.add_hotkey('f11', play_sound, args=[10])
    keyboard.add_hotkey('f12', play_sound, args=[11])
    keyboard.add_hotkey(72, select_move, args=[[0, -1]])
    keyboard.add_hotkey(80, select_move, args=[[0, 1]])
    keyboard.add_hotkey(77, select_move, args=[[1, 0]])
    keyboard.add_hotkey(75, select_move, args=[[-1, 0]])
    keyboard.add_hotkey(76, play_sound, args=[menu[select[0]][select[1]]])
    keyboard.add_hotkey(73, sd.stop)

def main():                                 # Интерфейс
    sounds = sound_get(True)[1]

    combo = 0
    for i in sounds:
        index = COMBOS[combo].findText(i)
        COMBOS[combo].setCurrentIndex(index)
        combo += 1

    x = threading.Thread(target=key, args=(1,))
    x.setDaemon(True)
    x.start()
    win.save_button.clicked.connect(save)

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
        win.combo11,
    ]

    menu = sound_get(True)[2]

    main()
    sys.exit(app.exec())
