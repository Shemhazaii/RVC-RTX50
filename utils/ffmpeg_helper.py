import os
import platform
import shutil

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if platform.system() == "Windows":
    FFMPEG = os.path.join(ROOT, "tools", "ffmpeg.exe")
    FFPROBE = os.path.join(ROOT, "tools", "ffprobe.exe")
else:
    FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
    FFPROBE = shutil.which("ffprobe") or "ffprobe"