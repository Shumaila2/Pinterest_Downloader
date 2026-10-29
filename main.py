# main.py
import sys
import os

# Needed for --noconsole builds: gives Python somewhere to "print" to
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

import webview
from paths import resource_path

PIN_HTML = "file:///" + resource_path("pin_video_down", "style", "pin_index.html").replace("\\", "/")


def run_app():
    """
    Opens the downloader window straight away (no login needed).
    The optional login window is opened later, from the
    "Log in (optional)" button inside the downloader.
    """
    # import locally so GUI libs aren't touched before start
    from pin_video_down.pin_video_downloader_GUI import pin_down, after_loaded

    api = pin_down()
    win = webview.create_window("Pinterest Downloader", PIN_HTML, js_api=api)
    api._window = win
    win.events.loaded += lambda: win.evaluate_js("backendReady()")
    webview.start(after_loaded, debug=False, gui="edgechromium")


if __name__ == "__main__":
    run_app()