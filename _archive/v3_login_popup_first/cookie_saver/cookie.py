import json
import os
import webview
import requests


class cookie_saver:
    def __init__(self, cookie_file):
        self.cookies = {}
        self.cookie_file = cookie_file
        
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.pinterest.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }

    
    def parse_cookie_string(self, cookie_input):
        """
        Accepts either a raw cookie string or dict and returns a valid dict for requests.
        """
        if isinstance(cookie_input, dict):
            return cookie_input

        cookies = {}
        if isinstance(cookie_input, str):
            parts = cookie_input.split(";")
            for part in parts:
                if "=" in part:
                    k, v = part.strip().split("=", 1)
                    cookies[k.strip()] = v.strip()
        return cookies

    
    def is_logged_in(self, cookies, timeout=10):
        """
        Returns {"logged_in": bool, "type": "logged_in" | "public" | "invalid", "info": str}
        """
        required_keys = ["_pinterest_sess"]
        for k in required_keys:
            if k not in cookies or len(cookies[k]) < 20:
                return {"logged_in": False, "type": "invalid", "status": 0,
                        "info": f"missing or invalid cookie: {k}"}
    
        try:
            url = "https://www.pinterest.com/"
            r = requests.get(url, cookies=cookies, headers=self.HEADERS, timeout=timeout)
            html = r.text.lower()
    
            # Wrong / gibberish cookies
            if r.status_code != 200:
                return {"logged_in": False, "type": "invalid", "status": r.status_code,
                        "info": f"http {r.status_code}"}
    
            # Logged-in detection
            if any(x in html for x in ["logout", "/settings/", "your profile", "pin-builder", "create idea pin"]):
                return {"logged_in": True, "type": "logged_in", "status": 200,
                        "info": "user session active"}
    
            # Visitor/public detection
            elif any(x in html for x in ["log in", "sign up", "email or password"]):
                return {"logged_in": False, "type": "public", "status": 200,
                        "info": "visitor/public session"}
            
            else:
                return {"logged_in": False, "type": "invalid", "status": r.status_code,
                    "info": "could not determine login state from page content"}
    
        except Exception as e:
            return {"logged_in": False, "type": "invalid", "status": 0, "info": f"error: {e}"}


    def can_access_resource(self, cookies, resource_url, timeout=10):
        """
        Check whether given cookies can access a specific resource (pin URL).
        Returns {"accessible": bool, "status": int, "reason": str}
        """
        try:
            r = requests.get(resource_url, cookies=cookies, headers=self.HEADERS, timeout=timeout, allow_redirects=True)
            status = r.status_code
            print(f"DEBUG: resource {resource_url} -> {status} final:{r.url}")
            lower = r.text[:2000].lower() if r.text else ""
            
            # heuristic rules for restricted/private content
            if status == 200:
                if ("only visible to" in lower) or ("login" in lower) or ("forbidden" in lower) or ("invalid resource request" in lower):
                    return {"accessible": False, "status": status, "reason": "content appears restricted or requires login"}
                return {"accessible": True, "status": 200, "reason": "ok"}
            else:
                return {"accessible": False, "status": status, "reason": f"http {status}"}
        except Exception as e:
            print("DEBUG: resource request error:", e)
            return {"accessible": False, "status": 0, "reason": f"error: {e}"}
    
        
    def save_cookies(self, cookies):
     """
     Validate and save cookies. If saved successfully, close the cookie window and
     create the downloader window (no webview.start() calls).
     Returns the same dict you already used for the front-end JS to display messages.
     """
     cookies = self.parse_cookie_string(cookies)
     result = self.is_logged_in(cookies)

     if result["type"] == "logged_in":
         # Save to file
         with open(self.cookie_file, "w") as f:
             json.dump(cookies, f)

         # Now create the downloader window WITHOUT calling webview.start()
         try:
             from pin_video_down.pin_video_downloader_GUI import pin_down
             # compute HTML path relative to project
             from paths import resource_path
             html_path = "file:///" + resource_path("pin_video_down", "style", "pin_index.html").replace("\\", "/")

             api2 = pin_down()
             win2 = webview.create_window("Pinterest Downloader", html_path, js_api=api2)
             api2.window = win2
             # fires as soon as THIS window's DOM is actually ready
             win2.events.loaded += lambda: win2.evaluate_js("backendReady()")
         except Exception as e:
             print("DEBUG: error creating downloader window:", e)

         return {"status": True, "message": "✅ Cookies saved — logged in!", "redirect": True}

     if result["type"] == "public":
         return {"status": False,
                 "message": "⚠️ These cookies work, but you're not logged in — private pins won't be accessible. Log into Pinterest in your browser first, then re-copy the cookies.",
                 "redirect": False}

     return {"status": False, "message": "❌ Invalid cookies. Please paste fresh ones from your browser.", "redirect": False}


    def get_saved_cookies(self):
        """Return cookies if already saved"""
        if os.path.exists(self.cookie_file):
            try:
                with open(self.cookie_file, "r") as f:
                    return json.load(f)
                
            except Exception as e:
                print("DEBUG: error loading cookie file:", e)
                return {}
        return {}
        
    # def open_downloader(self):
        
    #     from pin_video_down.pin_video_downloader_GUI import pin_down, after_loaded
    
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     ROOT = os.path.dirname(BASE_DIR)
    
    #     html_path = os.path.join(ROOT, "pin_video_down", "style", "pin_index.html")
        
    #     api2 = pin_down()
    #     webview.create_window("Pinterest Downloader", html_path, js_api=api2)
    #     webview.start(after_loaded, debug=False, gui="edgechromium")

if __name__ == "__main__":
    
    api = cookie_saver(cookie_file="D:\cookies.json")
    window = webview.create_window(
        "Pinterest Downloader Setup",
        url="style/cookie_index.html",
        width=700,
        height=500,
        js_api=api,
    )
    webview.start()

