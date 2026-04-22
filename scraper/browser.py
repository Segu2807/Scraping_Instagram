import json
import os
from playwright.sync_api import sync_playwright

class InstagramBrowser:
    def __init__(self, headless=False):
        self.headless = headless
        self.cookies_file = "data/instagram_cookies.json"
        self.context = None
        self.page = None
        self.playwright = None
        self.browser = None

    def _save_cookies(self, context):
        """Guarda las cookies en formato JSON vertical"""
        cookies = context.cookies()
        with open(self.cookies_file, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        print(f"✅ Cookies guardadas en {self.cookies_file} (formato vertical)")

    def _load_cookies(self, context):
        """Carga las cookies desde el archivo JSON"""
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print("✅ Cookies cargadas. Sesión restaurada.")
            return True
        return False

    def start(self):
        """Inicia el navegador y carga la sesión"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = self.context.new_page()

        if self._load_cookies(self.context):
            self.page.goto("https://www.instagram.com/")
            self.page.wait_for_timeout(3000)
            return

        print("🔐 No se encontraron cookies. Inicia sesión MANUALMENTE...")
        self.page.goto("https://www.instagram.com/accounts/login/")
        input("✅ Presiona ENTER después de iniciar sesión...")
        self._save_cookies(self.context)

    def get_page(self):
        return self.page

    def close(self):
        """Cierra el navegador y guarda cookies"""
        try:
            if self.page and self.context:
                cookies = self.context.cookies()
                with open(self.cookies_file, "w", encoding="utf-8") as f:
                    json.dump(cookies, f, indent=2, ensure_ascii=False)
                print("✅ Cookies guardadas antes de cerrar")
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"Error al cerrar: {e}")