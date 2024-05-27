import sys
import time
import os

from loguru import logger
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


load_dotenv()

class Istscraper:
    def __init__(self):
        logger.remove()
        logger.add('ist_scraper.log', rotation='700kb', level='WARNING')
        logger.add(sys.stderr, level='INFO')

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_followers(self, url: str):
        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)

            # login user by credentials
            input_username = wait.until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
            input_username.clear()
            input_username.send_keys(os.getenv('username'))
            input_username.send_keys(Keys.ENTER)
            input_password = wait.until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
            input_password.clear()
            input_password.send_keys(os.getenv('password'))
            input_password.send_keys(Keys.ENTER)

            # after log in  we are trying to don't save info
            n_path = "//div[@class='_ac8f']//div[contains(@class,'x1i10hfl')][contains(text(),'Not now')]"
            info_button = wait.until(ec.element_to_be_clickable((By.XPATH, n_path)))
            info_button.click()
            time.sleep(5)

            notif_path = '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
            notif_button = wait.until(ec.element_to_be_clickable((By.XPATH, notif_path)))
            if notif_button:
                notif_button.click()
                logger.info('user is successfully login ')

                # click on profile button
                p_path = ("//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985"
                          " xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 "
                          "x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x5n08af xwhw2v2 x6ikm8r x10wlt62 xlyipyv"
                          " x9n4tj2 _a6hd']")
                profile_button = wait.until(ec.element_to_be_clickable((By.XPATH, p_path)))
                profile_button.click()

                # extract the post number
                pos_css = "li.xl565be.x1m39q7l.x1uw6ca5.x2pgyrj span._ac2a"
                post_count_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, pos_css)))
                follower_count = post_count_element.text
                logger.info(f'the number of post is: {follower_count}')

                # extract the follower number
                p_css = "li.xl565be.x1m39q7l.x1uw6ca5.x2pgyrj:nth-child(2) span._ac2a"
                follower_count_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, p_css)))
                follower_count = follower_count_element.text
                logger.info(f'the number of followers is: {follower_count}')

                # extract the following number
                p_css1 = "li.xl565be.x1m39q7l.x1uw6ca5.x2pgyrj:nth-child(3) span._ac2a"
                following_count_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, p_css1)))
                following_count = following_count_element.text
                logger.info(f'the number of following is: {following_count}')
            else:
                logger.error("error to login user !")
        except Exception as e:
            logger.error(f'Error to fetch content from {url}: {e}')

    def clode(self):
        self.driver.close()


scraper = Istscraper()
scraper.get_followers("https://www.instagram.com/")
scraper.clode()
