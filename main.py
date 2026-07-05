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
            print("📲 Message envoyé sur Discord")
        except:
            print("⚠️ Erreur Discord")

    def scrape_winamax(self, max_matches=30):
        try:
            print(f"🌐 Chargement de Winamax (max {max_matches} matchs)...")
            self.driver.get("https://www.winamax.fr/")
            time.sleep(12)

            matches = []
            events = self.driver.find_elements(By.CSS_SELECTOR, "div.market, div.event, .odd, .fixture, .bet-card")

            for event in events[:max_matches]:
                try:
                    teams = event.find_elements(By.CSS_SELECTOR, ".team-name, .participant, .team, .event-name")
                    odds = event.find_elements(By.CSS_SELECTOR, ".odd, .price, .bet-odd, button")

                    if len(odds) >= 3 and len(teams) >= 2:
                        matches.append({
                            "match": f"{teams[0].text.strip()} - {teams[1].text.strip()}",
                            "home": float(odds[0].text.replace(',', '.')),
                            "draw": float(odds[1].text.replace(',', '.')),
                            "away": float(odds[2].text.replace(',', '.')),
                        })
                except:
                    continue

            print(f"✅ {len(matches)} matchs récupérés")
            return pd.DataFrame(matches)
        except Exception as e:
            print("Erreur scraping:", e)
            return pd.DataFrame()

    def analyze(self):
        df = self.scrape_winamax(max_matches=30)
        if df.empty:
            self.send_discord("⚠️ Aucun match trouvé sur Winamax.")
            return

        alert_count = 0
        for _, row in df.iterrows():
            total = 1/row['home'] + 1/row['draw'] + 1/row['away']
            value = row['home'] - (1 / (1/row['home'] / total))
            
            if value > 0.07:  # Seuil un peu plus bas pour plus d'alertes
                alert_count += 1
                msg = f"""🔥 **VALUE BET #{alert_count}**
Match : {row['match']}
Cote 1 : {row['home']:.2f} | Value : +{value:.3f}"""
                self.send_discord(msg)

        self.send_discord(f"📊 Analyse terminée : {len(df)} matchs scannés, {alert_count} value bets trouvées.")

    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    bot = WinamaxBot()
    bot.analyze()
    time.sleep(600)  # 10 minutes
    bot.close()
