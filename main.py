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
            time.sleep(12)  # Attente pour chargement

            matches = []
            events = self.driver.find_elements(By.CSS_SELECTOR, "div.market, div.event, .odd")

            for event in events[:10]:
                try:
                    teams = event.find_elements(By.CSS_SELECTOR, ".team-name, .participant")
                    odds = event.find_elements(By.CSS_SELECTOR, ".odd, .price")

                    if len(odds) >= 3 and len(teams) >= 2:
                        matches.append({
                            "match": f"{teams[0].text} - {teams[1].text}",
                            "home": float(odds[0].text.replace(',', '.')),
                            "draw": float(odds[1].text.replace(',', '.')),
                            "away": float(odds[2].text.replace(',', '.')),
                        })
                except:
                    continue
            return pd.DataFrame(matches)
        except:
            return pd.DataFrame()

    def analyze(self):
        df = self.scrape_winamax()
        if df.empty:
            self.send_discord("⚠️ Aucun match trouvé sur Winamax.")
            return

        for _, row in df.iterrows():
            total = 1/row['home'] + 1/row['draw'] + 1/row['away']
            value = row['home'] - (1 / (1/row['home'] / total))
            
            if value > 0.08:
                msg = f"""🔥 **VALUE BET WINAMAX !**
Match : {row['match']}
Cote 1 : {row['home']:.2f} | Value : +{value:.3f}"""
                self.send_discord(msg)

    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    bot = WinamaxBot()
    bot.analyze()
    time.sleep(300)  # Garder en vie
    bot.close()
