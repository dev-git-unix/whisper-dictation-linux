#!/usr/bin/env python3
import os
import subprocess
import threading
import time
from faster_whisper import WhisperModel
from pystray import Icon
from PIL import Image, ImageDraw

# --- Config ---
MODEL_SIZE = "tiny"           # fastest for CPU
AUDIO_FILE = "/tmp/dictation.wav"

# --- Mic Icon ---
def create_mic_icon():
    image = Image.new('RGB', (64, 64), color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16,16,48,48), fill='red')
    return image

icon = Icon("mic", create_mic_icon())

def show_icon():
    icon.run_detached()

def hide_icon():
    icon.stop()

# --- Record audio ---
def record_audio(duration=10):
    subprocess.call([
        "ffmpeg", "-f", "pulse", "-i", "default", "-t", str(duration),
        "-ac", "1", "-ar", "16000", AUDIO_FILE
    ])

# --- Transcribe ---
def transcribe():
    model = WhisperModel(MODEL_SIZE, device="cpu")
    segments, _ = model.transcribe(AUDIO_FILE, beam_size=5)
    text = " ".join([seg.text for seg in segments])
    # Copy to clipboard
    clip_cmd = "wl-copy" if os.environ.get("WAYLAND_DISPLAY") else "xclip -selection clipboard"
    subprocess.run(clip_cmd, input=text.encode(), shell=True)
    print("📝", text)

# --- Main ---
def main():
    print("🎙️ Listening for dictation...")
    show_icon()
    record_audio(duration=5)  # record 5 sec for fast response
    hide_icon()
    transcribe()
    print("✅ Dictation finished. Text copied to clipboard.")

if __name__ == "__main__":
    main()

