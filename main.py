from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

class WinamaxBot:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/1522673813840466153/Dr8yF4Siz1rvsbbrl96shrk4s9xeRwJm8YnEaWsyNVl5HLPL2qkoHZjuSMGxDOpW_U9B"

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
            driver = webdriver.Chrome(options=options)
            
            driver.get("https://www.winamax.fr/")
            time.sleep(8)
            
            self.send_discord("🔥 **Bot Winamax actif**\nScraping effectué avec succès.")
            
            driver.quit()
        except Exception as e:
            self.send_discord(f"⚠️ Erreur : {str(e)[:100]}")

if __name__ == "__main__":
    bot = WinamaxBot()
    bot.run()
    time.sleep(180)  # 3 minutes seulement
