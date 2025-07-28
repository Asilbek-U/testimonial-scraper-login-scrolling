import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
import sys

start_time = time.time()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.110 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/117.0"
]

options = uc.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1800")
options.add_argument(f"user-agent={random.choice(user_agents)}")
# options.add_argument("--headless=new")

driver = uc.Chrome(options=options)

url = "https://web-scraping.dev/login"
driver.get(url)

try:
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
except Exception as e:
    print(f"Failed to find fields: {e}")
    driver.quit()
    sys.exit()

USERNAME = "user123"
PASSWORD = "password"

username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)


login_button.click()

time.sleep(random.uniform(2,3))

if "Logout" in driver.page_source:
    print("Logged in")
else:
    print("Something went wrong")
    driver.quit()
    sys.exit()

driver.get("https://web-scraping.dev/testimonials")

last_count = 0

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1.5, 3.5))

    reviews = driver.find_elements(By.CLASS_NAME, "testimonial")
    new_count = len(reviews)

    if last_count == new_count:
        break

    last_count = new_count

rows = []

for review in reviews:
    rating_element = review.find_elements(By.CSS_SELECTOR, "span.rating > svg")
    rating = len(rating_element)
    
    text = review.find_element(By.CLASS_NAME, "text").text.strip()

    rows.append({"Review": text, "Rating": rating})

driver.quit()

end_time = time.time()
duration = end_time - start_time
minutes = int(duration // 60)
seconds = int(duration % 60)
print(f"Scraping took {minutes} minutes and {seconds} seconds")

df = pd.DataFrame(rows)
df.to_excel("testimonials.xlsx", index=False)
