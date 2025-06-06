import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def check_portfel(driver, url):
    driver.get(url)
    time.sleep(3)
    today = datetime.now().strftime("%d.%m.%Y")
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")[1:]
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 6:
            data = cols[5].text.strip()
            if data == today:
                spol = cols[0].text.strip()
                cena = cols[3].text.strip()
                send_telegram_message(f"📢 Nowy zakup!\nSpółka: {spol}\nCena: {cena}\nŹródło: {url}")

def main():
    try:
        driver = get_driver()
        driver.get("https://strefainwestorow.pl/user/login")
        time.sleep(2)

        driver.find_element(By.NAME, "name").send_keys(EMAIL)
        driver.find_element(By.NAME, "pass").send_keys(PASSWORD)
        driver.find_element(By.ID, "edit-submit").click()
        time.sleep(3)

        portfele = [
            "https://strefainwestorow.pl/portfel_strefy_inwestorow",
            "https://strefainwestorow.pl/portfel_petard"
        ]
        for url in portfele:
            check_portfel(driver, url)

        driver.quit()

    except Exception as e:
        send_telegram_message(f"❌ Błąd:\n{e}")

if __name__ == "__main__":
    main()
