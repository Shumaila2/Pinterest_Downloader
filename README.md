<div align="center">

# 📌 Pinterest Downloader

**Save Pinterest video pins to your PC, with sound** 🎬

![Python](https://img.shields.io/badge/Python-3.12-b82e43?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-only-b82e43?logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/Status-v4%20working-2f7a16)

</div>

A small Windows desktop app that downloads Pinterest video pins into a folder you choose.

The project started as a command-line script that could download **private pins**, and slowly grew into a desktop app with an optional login, a backup downloader, its own icon, and a standalone `.exe`.

**Current Version: v4 — Working**

---

## ✨ Features

* 🎬 Downloads public pins as MP4 **with sound**
* 📌 Works with pins from public boards
* 🖥️ Simple window: pick a folder, paste a link, click Download
* 📊 Live progress bar while downloading
* 🔑 Login is **optional**, public pins need no account
* 🚪 Log in / Log out buttons, with the current status shown in the window
* 🔁 Two download methods: if the first one fails, a backup tries
* 💬 Clear messages when a pin can't be downloaded
* 📦 Standalone `.exe` with ffmpeg included, nothing to install
* 🎀 Custom icon and a pink theme

---

## 🧠 How It Works

```text
Pin link
   ↓
yt-dlp            →  MP4 with sound
   ↓ if it fails
pinterest-dl      →  backup (may save a silent video or an image)
   ↓ if it fails too
A friendly message explaining what happened
```

The window is made with `pywebview`: the page you see is HTML/CSS/JS, and the downloading happens in Python behind it.

---

## 🔑 Optional Login

Public pins download without logging in. The **Log in (optional)** button is only for pins tied to your account, and private pins may still fail.

* You paste four cookie values from your browser (`csrftoken`, `_pinterest_sess`, `_auth`, `_routing_id`). The login window explains how.
* Only a real logged-in session is accepted.
* **Log out** deletes the saved cookies. It does not log you out of Pinterest in your browser.

📍 **Where cookies are saved:** on every user's own PC, in their AppData folder:

```text
%APPDATA%\PinterestDownloader\cookies.json
```

(Type `%APPDATA%` into File Explorer to open it.) Cookies are never stored inside the app folder or the `.exe`, so nothing private is shared when you share the app. They work like a password, so never share them.

---

## 📁 Project Structure

```text
Pinterest_Downloader/
│
├── main.py
├── paths.py
├── requirements.txt
├── icon.ico
│
├── cookie_saver/
│   ├── cookie.py
│   └── style/
│       ├── cookie_index.html
│       ├── script.js
│       └── style.css
│
├── pin_video_down/
│   ├── pin_video_downloader_GUI.py
│   ├── ffmpeg.exe
│   ├── ffprobe.exe
│   └── style/
│       ├── pin_index.html
│       ├── style.css
│       └── dev-icon-89 (1).svg
│
└── _archive/
    ├── pin_downloader_v1_cli.py
    ├── pin_downloader_v2_gui_ytdlp.py
    └── v3_login_popup_first/
```

| File / Folder                   | Purpose                                                              |
| ------------------------------- | -------------------------------------------------------------------- |
| `main.py`                       | Starts the app and opens the downloader window                       |
| `paths.py`                      | Finds the bundled files and the cookie location (works in the `.exe` too) |
| `requirements.txt`              | Python packages the project needs                                    |
| `icon.ico`                      | The app icon                                                         |
| `cookie_saver/`                 | The optional login window                                            |
| `pin_video_down/`               | The downloader: download logic, main window, and ffmpeg              |
| `pin_video_downloader_GUI.py`   | Both download methods, and the actions the window can trigger        |
| `ffmpeg.exe`, `ffprobe.exe`     | Merge Pinterest's separate video and audio into one MP4              |
| `_archive/`                     | Old versions, not used by the app                                    |

> Keep the folder names `cookie_saver` and `pin_video_down` as they are. The code and the build command depend on them.

---

## 🔄 Version History

### v1 — Command-Line Version

The very first version: a command-line script using `yt-dlp` with the login cookies written directly in the code. It **successfully downloaded private pins**, which is why the project continued.

### v2 — First Desktop Window

Started turning the script into a desktop app: a window with a folder picker, a link box, a live progress bar, and a cookie setup page. While finishing it, an error appeared, and when I came back to fix it, private pins could no longer be downloaded. `yt-dlp` now got a "404 Not Found" error from Pinterest, even with valid login cookies. Public pins still worked.

### v3 — Packaged App

Fixed the early bugs and added `pinterest-dl` as a backup downloader. Cookies moved into AppData, and the app was packaged into a standalone `.exe` with ffmpeg included. The login window still appeared first, and it was required.

### v4 — Optional Login *(current)*

Removed the forced login, since public pins don't need an account. Added the Log in / Log out buttons with a status line, clearer error messages, and a cleaner look for the login area.

---

## 🛠️ Technologies Used

* 🐍 Python 3.12
* 🪟 pywebview (the window)
* ⬇️ yt-dlp and pinterest-dl (the downloaders)
* 🎞️ ffmpeg (merges video and audio)
* 🌐 HTML, CSS and JavaScript
* 📦 PyInstaller (builds the `.exe`)

---

## ⚙️ Setup

### Run from source

```bash
python -m venv build_env
build_env\Scripts\activate
pip install -r requirements.txt
python main.py
```
<details>
<summary>📦 Build the .exe yourself</summary>

Delete any old `build`, `dist` and `.spec` first, then run this from the project folder:

```bash
pyinstaller --noconsole --icon icon.ico --name PinterestDownloader --add-data "pin_video_down\style;pin_video_down\style" --add-data "cookie_saver\style;cookie_saver\style" --add-data "pin_video_down\ffmpeg.exe;pin_video_down" --add-data "pin_video_down\ffprobe.exe;pin_video_down" --collect-all pinterest_dl --collect-all yt_dlp --hidden-import pin_video_down.pin_video_downloader_GUI --hidden-import cookie_saver.cookie main.py
```

The finished app is the whole `dist\PinterestDownloader` folder. To share it, zip that folder.

</details>

## 📥 Download

Just want the app? Open the **[latest release](https://github.com/Shumaila2/Pinterest_Downloader/releases/latest)**, download `Pinterest_Downloader.exe`, and run it. No Python or ffmpeg needed.

> Windows may show "Windows protected your PC" the first time, because the app is unsigned. Click *More info*, then *Run anyway*.

---

## ⚠️ Current Limitations

* ❌ Private pins and pins from private boards can't be downloaded right now, even when logged in
* 🔇 The backup downloader may save a silent video or an image
* 🔑 Saved cookies can expire, and the app only notices when a private pin fails
* 🪟 Windows only

---

## 🔮 Future Improvements

> Features listed here are **not part of v4 unless they are actually implemented.**

* 🎯 **Main goal:** download private pins. This is still the goal. It isn't possible right now, but I may come back to it later, maybe with a different approach.
* 🌍 **Bigger idea:** go beyond Pinterest and combine more social media sites in one app.

---

## 🏁 v4 — Working

v4 is the current working version of the project.

The project will only need changes when there is a **real bug, a way to download private pins again, or a practical reason to change how it works.**
