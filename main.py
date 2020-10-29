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
def find_device():
    '''
    Ищем устройство device и возвращаем его индекс
    '''

    list_ = list(sd.query_devices())    # Список устройств вывода звука
    device = 'VoiceMeeter Input'        # Имя искомого устройства

    msg = QtWidgets.QMessageBox()       # Окно ошибки (Устройство не найдено)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't install VoiceMeeter")
    msg.setInformativeText('install VoiceMetter from "redist" folder or download it from \nvb-audio.com/Voicemeeter')
    msg.setWindowTitle('Error')

    for i in list_:
        if device in i['name']:
            return i['name']
    
    msg.exec_()
    exit()

def sound_get():
    '''
    Сбор всех аудифайлов
    '''
    def check_format(name, format_):
        '''
        Проверка формата файла name
        name - название файла, только название
        format_ - нужный формат
        '''
        suf = ''                        # Суффикс
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
    
    def sound_convert(path, name, format_):
        '''
        Конвертация файла name в папке path в формат format_
        по средством ffmpeg.exe

        path - папка с файлом, может содержать полный или относительный путь
        name - название файла, может только название файла
        format_ - формат в который нужно конвертировать
        '''
        if os.path.exists('ffmpeg.exe'):
            old_name = name
            if check_format(name, ['mp3', 'm4a']):
                while name[-1] != '.':
                    name = name[:-1]
                name += format_

                os.system(f'ffmpeg.exe -i "{os.path.join(path, old_name)}" "{os.path.join(path, name)}"')
                os.remove(f'{os.path.join(path, old_name)}')
            return name
    
    msg = QtWidgets.QMessageBox()       # Окно ошибки (Не найдены файлы в папке 'sound')
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("You don't have any sounds in 'sound' folder")
    msg.setInformativeText('download sound in .wav / .mp3 / .m4a format')
    msg.setWindowTitle('Error')
    
    ffmsg = QtWidgets.QMessageBox()     # Окно ошибки (Не найден ffmpeg.exe)
    ffmsg.setIcon(QtWidgets.QMessageBox.Warning)
    ffmsg.setText("You don't have ffmpeg.exe in the program root folder")
    ffmsg.setInformativeText('download ffmpeg from ffmpeg.org for converting sound files')
    ffmsg.setWindowTitle('Error')

    if os.path.exists('sound'):
        if len(os.listdir('sound')) == 0:
            msg.exec_()

        menu = []                       # Оверлейное меню
        sounds_list = ['sound\\']       # Начальная категория
        sounds = []                     # Все аудиофайлы
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

def save():
    '''
    Сохранение настроек оверлея и глобальных хоткеев
    '''
    hotkeys = {}                        # Словарь хоткеев и аудиофайлов
    sounds = jsonread('settings.json')['sounds']# Все аудиофайлы
    KEYS_JSON = {}                      # Настроенные клавиши

    for i in range(len(COMBOS)):
        hotkeys.setdefault(HOTKEYS[i].text(), COMBOS[i].currentText())

    for i in KEYS_CMD.keys():
        KEYS_JSON.setdefault(COMMAND_DICT[i], KEYS_CMD[i])

    sounds_list = {'sounds':sounds, 'hotkeys':hotkeys, 'menu':menu, 'KEYS_CMD':KEYS_JSON}
    jsonwrite('settings.json', sounds_list)

def play_sound(index):
    '''
    Проигрывание звука
    index - может быть индексом комбобокса с именем
        или '' для проигрывания выбранного в оверлее имени
    '''
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

def hotkey_remap(btn):
    '''
    Переназначение хоткея
    btn - индекс кнопки хоткея в списке HOTKEYS
    '''
    def check(key):
        '''
        Проверка кнопки btn на не участие 
            в списке запрещенных клавиш keys.forbidden
            если это клавиша 'Key.backspace' то стираем значение
        key - pynput код клавиши
        '''
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
    '''
    Поиск ключа в словаре dict по значению val
    dict - словарь
    val - значение
    '''
    return next(key for key, value in dict.items() if value == val)


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
    '''
    Проверка клавиши key на наличие записанных функций
    key - pynput код клавиши
    '''
    key = str(key).replace("'",'')  # Преобразование кода в строку
    key_n = ''                      # Переведенное значение клавиши
    try:
        key_n = keys.dict_[key]
    except KeyError:
        pass
    if key_n in HOTKEYS_CMD:
        play_sound(HOTKEYS_CMD.index(key_n))
    elif key in KEYS_CMD.values():
        find_key(KEYS_CMD, key)()

def main():
    '''
    Открытие окна win, запуск слушателя клавиатуры,
        подключение кнопок интерфейса к функциям
    '''
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
    app = QtWidgets.QApplication([])    # Приложение
    over = OverlayUi()                  # Окно оверлея
    pref = PreferencesUi()              # Окно настроек
    win = MainUi()                      # Основное окно
    COMBOS = [                          # Список комбобоксов в win
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
    HOTKEYS = [                         # Список кнопок хоткеев в win
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
    PREF_BTN = [                        # Список кнопок настроек клавиш в pref
        pref.select_move_up,
        pref.select_move_down,
        pref.select_move_left,
        pref.select_move_right,
        pref.play_sound,
        pref.stop_sound,]

    ### Поиск устроства ввода ###
    sd.default.device = find_device()   # Установка устройства вывода по умолчанию
    sound_get()                         # Сбор всех аудиофайлов

    ### Глобальные переменные ###
    sound_get_dict = jsonread('settings.json')# Загрузка данных
    hotkeys = sound_get_dict['hotkeys'] # Загрузка словаря хоткеев
    menu = sound_get_dict['menu']       # Загрузка оверлейного меню
    select = [0, 0]                     # Установка курсора оверлея в нулевую позицию
    COMMAND_DICT = {                    # Словарь функций к строковому значению
            lambda: select_move((0, -1)):'select_move_up',      # вверх
            lambda: select_move((0, 1)) :'select_move_down',    # вниз
            lambda: select_move((-1, 0)):'select_move_left',    # влево
            lambda: select_move((1, 0)) :'select_move_right',   # вправо
            lambda: play_sound('')      :'play_sound',          # Играть
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

    ### Установка хоткеев ###
    combo = 0
    for i in hotkeys.items():
        index = COMBOS[combo].findText(i[1])
        COMBOS[combo].setCurrentIndex(index)
        HOTKEYS[combo].setText(i[0])
        combo += 1
    combo = None

    HOTKEYS_CMD = [                     # Имена связанные с хоткеями
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
