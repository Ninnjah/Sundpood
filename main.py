import os
import sys
import json
import threading
import keyboard
import soundfile as sf
import sounddevice as sd
from PyQt5 import QtWidgets, uic, QtGui, QtCore


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

def sound_get(filename, mode):              # Сбор файлов
    if os.path.exists(filename) and mode == False:
        sounds_list = jsonread(filename)
    elif not os.path.exists(filename) or mode == True:
        if os.path.exists('sound'):
            sounds = os.listdir('sound')
            if len(sounds) == 0:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("You don't have any sounds in 'sound' folder")
                msg.setInformativeText('download sound in .wav format')
                msg.setWindowTitle('Error')
                msg.exec_()
                exit()
            if os.path.exists('settings.json'):
                hotkeys = jsonread(filename)[1]
                sounds_list = [sounds, hotkeys]
            else:
                sounds_list = [sounds, ['', '', '', '', '', '', '', '', '', '', '', '']]

            for i in COMBOS:
                i.addItems(sounds)
            jsonwrite(filename, sounds_list)
        else:
            os.mkdir('sound')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("You don't have any sounds in 'sound' folder")
            msg.setInformativeText('download sound in .wav format')
            msg.setWindowTitle('Error')
            msg.exec_()
            exit()
    return sounds_list

def save():                                 # Сохранение списка хоткеев
    hotkeys = []
    sounds = sound_get('settings.json', False)
    for i in COMBOS:
        hotkeys.append(i.currentText())
    jsonwrite('settings.json', [sounds, hotkeys])
    sounds = None
    hotkeys = None

#def sounds_explore():                       # Оверлей
#    print('showing everlay')
#    overlay.show()

def play_sound(index):                      # Проигрываение звука
    filename = COMBOS[index].currentText()
    try:
        data, fs = sf.read(os.path.join('sound', filename), dtype='float32')  
        sd.play(data, fs)
        keyboard.wait(sd.play())
        sd.wait()
    except:
        pass

###! CONTROL !###

def key(arg):                               # Хоткеи
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
    keyboard.add_hotkey(73, sd.stop)
    #keyboard.add_hotkey('shift+f2', sounds_explore)
    keyboard.wait()
    main()

def main():                                 # Интерфейс
    win.start_button.setText('Save')
    win.show()
    sounds = sound_get('settings.json', True)[1]

    combo = 0
    for i in sounds:
        index = COMBOS[combo].findText(i)
        COMBOS[combo].setCurrentIndex(index)
        combo += 1

    x = threading.Thread(target=key, args=(1,))
    x.setDaemon(True)
    x.start()
    win.start_button.clicked.connect(save)


if __name__ == '__main__':
    # Поиск устроства ввода
    list_ = list(sd.query_devices())
    index = found_device(list_)
    sd.default.device = list_[index]['name']

    app = QtWidgets.QApplication([])
    win = uic.loadUi("sundpood.ui")
    #overlay = uic.loadUi("overlay.ui")
    #overlay.setWindowFlags(QtCore.Qt.ToolTip)

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

    main()
    sys.exit(app.exec())
