
---

### 🎙️ `dictate.py`
```python
#!/usr/bin/env python3
import os
import subprocess
from faster_whisper import WhisperModel

# Config
model_size = "tiny"
record_file = "/tmp/dictation.wav"

# Show notification when listening
subprocess.run(["notify-send", "🎙️ Whisper Dictation", "Listening..."])

# Record audio (10 seconds, change -t for longer/shorter)
subprocess.call([
    "ffmpeg", "-f", "pulse", "-i", "default",
    "-t", "10", "-ac", "1", "-ar", "16000",
    "-y", record_file
])

# Load model
model = WhisperModel(model_size, device="cpu")

# Transcribe
segments, _ = model.transcribe(record_file, beam_size=5)
text = " ".join([seg.text for seg in segments])

# Show transcription in terminal
print("📝", text)

# Copy to clipboard (Wayland or X11)
if os.environ.get("WAYLAND_DISPLAY"):
    subprocess.run(["wl-copy"], input=text.encode())
else:
    subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())

# Show notification when done
subprocess.run(["notify-send", "✅ Whisper Dictation", "Copied to clipboard!"])

