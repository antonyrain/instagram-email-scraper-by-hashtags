from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging
import random
import time
import csv
import re
import os


class Scraper:

    def __init__(self, service, options):
        self.driver = webdriver.Chrome(service=service, options=options)
        self.logger = logging.getLogger()

    def login_chrome(self, login, password):
        logger = self.logger
        driver = self.driver
        logger.info('Start')
        driver.implicitly_wait(5)
        driver.get('https://www.instagram.com')
        time.sleep(random.randrange(5, 7))

        # setting current tab as original
        original_window = driver.current_window_handle
        # creating the new empty tab and leave open
        driver.switch_to.new_window('tab')
        time.sleep(1)
        # back to original tab and go further
        driver.switch_to.window(original_window)
        time.sleep(1)

        logger.info('Authorization...')
        print('Authorization...')
        username_input = driver.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys(login)
        time.sleep(random.randrange(3, 6))
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(3, 6))
        password_input.send_keys(Keys.ENTER)

    def go_by_hashtag(self, hashtag):
        logger = self.logger
        driver = self.driver
        logger.info(f"Hashtag {hashtag}")
        print(f"\nHashtag {hashtag}")
        time.sleep(random.randrange(2, 4))
        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(random.randrange(2, 4))
        driver.find_element(By.CLASS_NAME, "v1Nh3").click()
        time.sleep(random.randrange(2, 4))

    def loop_by_feed(self, depth):
        driver = self.driver
        original_window = driver.current_window_handle
        try:
            counter = 1
            flag = 1
            emails_set = set()
            for i in range(depth):
                if counter % 5 == 0:
                    print(f"In progress: worked {counter} profiles")

                time.sleep(random.randrange(2, 4))
                instagram_feed_html = driver.page_source
                soup = BeautifulSoup(instagram_feed_html, "lxml")
                short_link = soup.find("a", class_="yWX7d").get("href")

                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break
                time.sleep(random.randrange(2, 4))

                driver.get(f"https://www.instagram.com{short_link}")
                driver.implicitly_wait(3)
                time.sleep(random.randrange(2, 4))
                instagram_profile_html = driver.page_source
                time.sleep(random.randrange(3, 5))
                emails_list = re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', instagram_profile_html)

                emails_set.clear()
                for i in emails_list:
                    emails_set.add(i)
                with open(f'emails.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    for item in emails_set:
                        writer.writerow([item])

                time.sleep(random.randrange(2, 4))
                driver.switch_to.window(original_window)
                time.sleep(random.randrange(2, 4))
                if flag == 1:
                    driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/button').click()
                else:
                    driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div[2]/button').click()
                flag = 2
                counter += 1
                time.sleep(random.randrange(2, 4))
        except:
            pass
        time.sleep(random.randrange(2, 4))

    def close_browser(self):
        logger = self.logger
        self.driver.close()
        self.driver.quit()
        logger.info("Finish")


def main():

    lang = "en-US"
    window_size = "1100,800"
    user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"

    options = Options()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable "Chrome is being controlled by automated test software" notification
    options.add_argument(f"--lang={lang}")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"--window-size={window_size}")
    prefs = {'disk-cache-size': 4096}
    options.add_experimental_option('prefs', prefs)
    # options.add_argument("--proxy-server=198.50.163.192:3129")  # set proxy
    # Creating and Configuring Logger
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename="logfile.log", filemode="w", format=log_format, level=logging.INFO)

    # options.headless = True  # Headless Mode. Driving Headless Browser
    options.add_argument("--headless")  # Headless Mode too
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))


    """
    _______________________________________________________________________
    ____________________Creating an instance of a class____________________
    _______________________________________________________________________
    """
    bot = Scraper(service, options)
    bot.login_chrome("lucky_accent", "likering22")
    file = open("hashtags.txt", "r", encoding="utf-8")
    for word in file:
        try:
            bot.go_by_hashtag(word)
            bot.loop_by_feed(11)
        except:
            pass
    bot.close_browser()


if __name__ == "__main__":
    main()