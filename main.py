from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime
import requests

class WinamaxBot:
    def __init__(self):
        self.driver = None
        self.webhook_url = "https://discord.com/api/webhooks/1522673813840466153/Dr8yF4Siz1rvsbbrl96shrk4s9xeRwJm8YnEaWsyNVl5HLPL2qkoHZjuSMGxDOpW_U9B"
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)

    def send_discord(self, message):
        try:
            requests.post(self.webhook_url, json={"content": message})
            print("📲 Notification Discord envoyée")
        except:
            print("⚠️ Erreur Discord")

    def scrape_winamax(self):
        try:
            print("🌐 Scraping Winamax...")
            self.driver.get("https://www.winamax.fr/")
            time.sleep(10)
            # Extraction simplifiée (à améliorer plus tard)
            return pd.DataFrame([{"match": "Test Match", "home": 2.1, "draw": 3.4, "away": 3.8}])
        except:
            return pd.DataFrame()

    def analyze(self):
        df = self.scrape_winamax()
        if df.empty:
            self.send_discord("⚠️ Aucun match trouvé.")
            return

        for _, row in df.iterrows():
            msg = f"""🔥 **TEST BOT WINAMAX**
Match : {row['match']}
Cote 1 : {row['home']}
Bot démarré avec succès !"""
            print(msg)
            self.send_discord(msg)

    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    bot = WinamaxBot()
    bot.analyze()
    bot.close()
