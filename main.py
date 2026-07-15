from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

class BetPawaBot:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/1522673813840466153/Dr8yF4Siz1rvsbbrl96shrk4s9xeRwJm8YnEaWsyNVl5HLPL2qkoHZjuSMGxDOpW_U9B"
        self.username = "0980330524"   # ← Remplace
        self.password = "2009"       # ← Remplace (risqué !)

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
            
            # Login
            driver.get("https://www.betpawa.com/")
            time.sleep(8)
            
            # Remplir login (adapte les sélecteurs)
            driver.find_element(By.NAME, "phone").send_keys(self.username)
            driver.find_element(By.NAME, "password").send_keys(self.password)
            driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(10)

            self.send_discord("✅ Connexion Bet Pawa réussie")

            # Ici tu peux ajouter la logique pour placer un coupon

            driver.quit()
        except Exception as e:
            self.send_discord(f"❌ Erreur login : {str(e)[:100]}")

if __name__ == "__main__":
    bot = BetPawaBot()
    bot.run()
    time.sleep(900)
