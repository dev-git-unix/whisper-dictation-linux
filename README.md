# Whisper Dictation Linux

macOS-style dictation for Ubuntu/Linux using Whisper. Press a hotkey, speak, and your words are transcribed and copied to clipboard.

## Features
- Works offline with [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- Hotkey support (double Ctrl or custom)
- Wayland & X11 clipboard

## Install
```bash
sudo apt update
sudo apt install ffmpeg python3-venv wl-clipboard xclip -y
python3 -m venv ~/whisper-env
source ~/whisper-env/bin/activate
pip install -r requirements.txt
```
## Usage
```bash
source ~/whisper-env/bin/activate
./dictate.py
```
## Hotkey Setup
Hotkey Setup

Map dictate.py to a keyboard shortcut in Settings → Keyboard → Shortcuts.
For double Ctrl, use xcape or interception-tools.
