import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
)

def dynamic_sleep(min_time: float = 0.5, max_time: float = 1.5) -> None:
    sleep_time = random.uniform(min_time, max_time)
    time.sleep(sleep_time)

def build_driver(headless: bool = True, user_agent: str = DEFAULT_UA) -> tuple[webdriver.Chrome, WebDriverWait]:
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--incognito")
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 15)
    return driver, wait

def handle_privacy_popup(wait: WebDriverWait) -> None:
    try:
        btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'agree')]")
            )
        )
        btn.click()
        dynamic_sleep(1, 3)
    except Exception:
        pass

def handle_location_prompt(wait: WebDriverWait) -> None:
    try:
        btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='NO THANKS']]"))
        )
        btn.click()
        dynamic_sleep(1, 3)
    except Exception:
        pass
