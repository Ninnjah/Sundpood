# Sundpood

![Banner](https://github.com/Ninnjah/Sundpood/blob/master/pics/banner.jpg)

App like [SoundPad](https://www.leppsoft.com/soundpad/en/download/)(needs [VoiceMeeter](https://vb-audio.com/Voicemeeter/)(allready in "redist" folder))

### Features:
- Play sound by pressing hotkey
- Supported formats:
  - .wav
  - .mp3
  - .m4a
- Converting sounds by [ffmpeg](https://ffmpeg.org/download.html)
- Sound categories (folders in "sound" folder)
- Overlay menu by press F1 key
- Overlay control on numpad (set in preferences)
- Light and Dark Themes

### Requirements:
- [sounddevice](https://pypi.org/project/sounddevice/) for playing sounds
- [pynput](https://pypi.org/project/pynput/) for hotkeys
- [PyQt5](https://pypi.org/project/PyQt5/) for GUI
- [VoiceMeeter](https://vb-audio.com/Voicemeeter/) for redirect sound into microphone
- [ffmpeg](https://ffmpeg.org/download.html) for convert sounds in .wav format
