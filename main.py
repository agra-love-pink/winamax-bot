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
        except:
            pass

    def scrape_winamax(self):
        try:
            self.driver.get("https://www.winamax.fr/")
            time.sleep(12)
            return pd.DataFrame([{"match": "Test", "home": 2.0, "draw": 3.5, "away": 4.0}])
        except:
            return pd.DataFrame()

    def analyze(self):
        df = self.scrape_winamax()
        self.send_discord("🔥 Bot Winamax en cours d'exécution...")

    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    while True:  # Boucle infinie pour Render
        bot = WinamaxBot()
        bot.analyze()
        bot.close()
        time.sleep(600)  # Attend 10 minutes entre chaque exécution
