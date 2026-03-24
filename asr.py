import os
import whisper
import subprocess

# ✅ Your FFmpeg bin path
FFMPEG_BIN_PATH = r"C:\Users\kashi\Downloads\ffmpeg-2026-02-04-git-627da1111c-full_build\bin"
os.environ["PATH"] = FFMPEG_BIN_PATH + os.pathsep + os.environ.get("PATH", "")

# Sanity check: ensure ffmpeg is callable
subprocess.run(["ffmpeg", "-version"], capture_output=True)

# Load Whisper model (CPU-safe)
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Robust Whisper transcription for Windows (no torchaudio).
    Skips fp16 and handles problematic files safely.
    """
    try:
        result = model.transcribe(
            audio_path,
            fp16=False,       # IMPORTANT for Windows CPU
            language="en"
        )
        text = result.get("text", "").strip()
        if not text:
            return "[No speech detected]"
        return text
    except RuntimeError:
        return "[Error processing this audio sample]"