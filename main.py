from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import re

class WinamaxBot:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/1522673813840466153/Dr8yF4Siz1rvsbbrl96shrk4s9xeRwJm8YnEaWsyNVl5HLPL2qkoHZjuSMGxDOpW_U9B"
        self.popular_leagues = ["Premier League", "Ligue 1", "Ligue 2", "Champions League", "Bundesliga", "Serie A", "La Liga"]

    def send_discord(self, message):
        try:
            requests.post(self.webhook_url, json={"content": message})
        except:
            pass

    def run(self):
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.winamax.fr/")
            time.sleep(15)

            matches = []
            events = driver.find_elements(By.CSS_SELECTOR, "div, button, .odd, .event, .fixture, .bet-card")

            for event in events[:45]:  # Jusqu'à 45 matchs
                try:
                    text = event.text
                    if any(league in text for league in self.popular_leagues):
                        # Extraction simple des cotes
                        odds = re.findall(r'\d+[,.]\d+', text)
                        if len(odds) >= 3:
                            matches.append({
                                "match": text.split('\n')[0] if '\n' in text else "Match inconnu",
                                "home": float(odds[0].replace(',', '.')),
                                "draw": float(odds[1].replace(',', '.')),
                                "away": float(odds[2].replace(',', '.')),
                            })
                except:
                    continue

            self.send_discord(f"✅ **Bot Winamax** - {len(matches)} matchs analysés (ligues populaires)")

            for match in matches[:5]:  # Envoie seulement les 5 meilleurs
                total = 1/match['home'] + 1/match['draw'] + 1/match['away']
                value = match['home'] - (1 / (1/match['home'] / total))
                if value > 0.07:
                    self.send_discord(f"🔥 Value Bet : {match['match']}\nCote 1 : {match['home']:.2f} | Value : +{value:.3f}")

            driver.quit()
        except Exception as e:
            self.send_discord(f"❌ Erreur : {str(e)[:100]}")

if __name__ == "__main__":
    bot = WinamaxBot()
    bot.run()
    time.sleep(900)  # 15 minutes
