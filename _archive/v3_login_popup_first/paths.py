import os
import sys


def resource_path(*parts):
    """Find files that ship with the app (HTML, ffmpeg...). Works in
    normal runs AND inside a PyInstaller build."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


def cookie_file_path():
    """Where the user's saved cookies live: a folder in AppData that the app
    creates by itself. Open it any time by typing %APPDATA% in File Explorer."""
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    folder = os.path.join(base, "PinterestDownloader")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "cookies.json")