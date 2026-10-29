# main.py
import sys
import os

# Needed for --noconsole builds: gives Python somewhere to "print" to
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

import webview
from paths import resource_path, cookie_file_path

PIN_HTML = "file:///" + resource_path("pin_video_down", "style", "pin_index.html").replace("\\", "/")
COOKIE_HTML = "file:///" + resource_path("cookie_saver", "style", "cookie_index.html").replace("\\", "/")
COOKIE_FILE = cookie_file_path()


def open_downloader_window():
    """
    Create the downloader window (no webview.start here).
    """
    # import locally to avoid early side-effects
    from pin_video_down.pin_video_downloader_GUI import pin_down, after_loaded

    api2 = pin_down()
    win = webview.create_window("Pinterest Downloader", PIN_HTML, js_api=api2)
    api2.window = win
    win.events.loaded += lambda: win.evaluate_js("backendReady()")
    # after_loaded will be executed once webview.start finishes and windows are loaded.
    # If you need immediate JS callback you can call win.evaluate_js(...) from API methods.


def run_app():
    """
    Centralized launcher: decides which window to open and calls webview.start() once.
    """
    # import cookie API locally (so DLLs / GUI libs not imported before start)
    from cookie_saver.cookie import cookie_saver

    api = cookie_saver(COOKIE_FILE)

    saved = api.get_saved_cookies()

    # CASE A: cookies already saved -> validate and open downloader directly
    if saved:
        result = api.is_logged_in(saved)
        if result["type"] in ["logged_in", "public"]:
            print("Valid cookies found → Opening downloader")
            open_downloader_window()
            # Single webview.start call - pass after_loaded from downloader module
            from pin_video_down.pin_video_downloader_GUI import after_loaded
            webview.start(after_loaded, debug=False, gui="edgechromium")
            return
        else:
            print("Cookies invalid → opening cookie setup")

    # CASE B: no cookies or invalid cookies -> open cookie setup window
    print("Opening cookie setup window")
    # create cookie API and window; cookie_saver.save_cookies() will create the downloader window
    cookie_api = api
    cookie_win = webview.create_window(
        "Pinterest Downloader Setup",
        url=COOKIE_HTML,
        width=700,
        height=500,
        js_api=cookie_api,
    )
    cookie_api.window = cookie_win

    # start event loop once. cookie_api.save_cookies() must create the downloader window
    # and close cookie window when cookies are saved.
    webview.start(debug=False, gui="edgechromium")


if __name__ == "__main__":
    run_app()

# from pin_video_down.pin_video_downloader_GUI import pin_down, after_loaded
# from cookie_saver.cookie import cookie_saver
# import webview
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PIN_HTML = os.path.join(BASE_DIR, "pin_video_down", "style", "pin_index.html")
# PIN_HTML = "file:///" + PIN_HTML.replace("\\", "/")

# COOKIE_HTML = os.path.join(BASE_DIR, "cookie_saver", "style", "cookie_index.html")
# COOKIE_HTML = "file:///" + COOKIE_HTML.replace("\\", "/")

# COOKIE_FILE = os.path.join(BASE_DIR, "cookie_saver", "cookies.json")

# api = cookie_saver(COOKIE_FILE)


# def open_downloader():
#     """
#     Opens the Pinterest downloader window from the MAIN THREAD.
#     """
#     api2 = pin_down()
#     win = webview.create_window("Pinterest Downloader", PIN_HTML, js_api=api2)
#     api2.window = win


# def after_main():
#     """
#     Called AFTER the cookie window closes.
#     This is where we check if cookies were saved.
#     """
#     saved = api.get_saved_cookies()

#     if saved:
#         result = api.is_logged_in(saved)
#         if result["type"] in ["logged_in", "public"]:
#             print("Cookies OK → Opening downloader")
#             open_downloader()
#         else:
#             print("Invalid cookies → reopening cookie setup")

#             win = webview.create_window(
#                 "Pinterest Downloader Setup",
#                 url=COOKIE_HTML,
#                 width=700,
#                 height=500,
#                 js_api=api,
#             )
#             api.window = win


# # ------------------------------------------------------------
# # MAIN LOGIC
# # ------------------------------------------------------------

# saved = api.get_saved_cookies()

# # Case 1: Cookies already exist
# if saved:
#     result = api.is_logged_in(saved)

#     if result["type"] in ["logged_in", "public"]:
#         print("Valid cookies found → Opening downloader")

#         open_downloader()
#         webview.start(after_loaded, debug=False, gui="edgechromium")

#     else:
#         print("Cookies invalid → Open setup")

#         win = webview.create_window(
#             "Pinterest Downloader Setup",
#             url=COOKIE_HTML,
#             width=700,
#             height=500,
#             js_api=api,
#         )
#         api.window = win

#         webview.start(after_main, debug=False, gui="edgechromium")

# # Case 2: No cookies at all
# else:
#     print("No cookies → Open setup")

#     win = webview.create_window(
#         "Pinterest Downloader Setup",
#         url=COOKIE_HTML,
#         width=700,
#         height=500,
#         js_api=api,
#     )
#     api.window = win

#     webview.start(after_main, debug=False, gui="edgechromium")
