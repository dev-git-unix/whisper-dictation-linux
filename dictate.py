#!/usr/bin/env python3
import os
import subprocess
import threading
from faster_whisper import WhisperModel
from pystray import Icon
from PIL import Image, ImageDraw

MODEL_SIZE = "tiny"
AUDIO_FILE = "/tmp/dictation.wav"

# --- Mic Icon ---
def create_mic_icon():
    image = Image.new('RGB', (64, 64), color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16,16,48,48), fill='red')
    return image

icon = Icon("mic", create_mic_icon())

def show_icon():
    icon.run()

def hide_icon():
    icon.stop()

# --- Record audio ---
def record_audio(duration=5):
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
    # show mic icon in a separate thread
    icon_thread = threading.Thread(target=show_icon, daemon=True)
    icon_thread.start()

    print("🎙️ Listening for dictation...")
    record_audio()
    hide_icon()
    transcribe()
    print("✅ Dictation finished. Text copied to clipboard.")

if __name__ == "__main__":
    main()

