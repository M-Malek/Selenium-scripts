import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Webdriver setup
chrome_webdriver_path = r""  # path to your
# chrome webdriver

driver = webdriver.Chrome(executable_path=chrome_webdriver_path)

# Twitter login - need to be fill in before use a script
twitter_login = ""  # your own twitter login
twitter_password = ""  # your own twitter password


class InternetSpeedTwitterBot:
    """Class to find and send internet info"""
    def __init__(self):
        self.speedtest_link = r'https://www.speedtest.net/'
        self.twitter_link = r'https://twitter.com/login'
        self.test_id = ""
        self.ping = ""
        self.download = ""
        self.upload = ""
        self.internet_message = ""

    def get_internet_speed(self):
        """Get internet stats from speedtest.net"""
        driver.get(self.speedtest_link)
        internet_accept_cookies = driver.find_element(By.CLASS_NAME, 'banner-actions-container')
        button_accept = internet_accept_cookies.find_element(By.ID, 'onetrust-accept-btn-handler')
        button_accept.click()

        internet_speed_button = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]'
                                                              '/div/div/div/div[2]/div[3]/div[1]/a/span[4]')
        internet_speed_button.click()

        time.sleep(60)

        my_internet_stats = driver.find_elements(By.CLASS_NAME, 'result-item-container')
        self.test_id = my_internet_stats[0].text.split("\n")[1]
        self.ping = my_internet_stats[1].text.split("\n")[1]
        self.download = my_internet_stats[2].text.split("\n")[1]
        self.upload = my_internet_stats[3].text.split("\n")[1]

        time.sleep(10)
        self.internet_message = f'My {self.test_id} internet speed test: PING: {self.ping}ms, ' \
                                f'download: {self.download} mbps,' \
                                f'upload: {self.upload} mbps.'

        # driver.close()

    def twitter_post(self, login, password):
        """Send your internet stats to Twitter"""
        # Login to twitter
        self.get_internet_speed()
        driver.get(self.twitter_link)
        time.sleep(10)
        pass_username = driver.find_element(By.TAG_NAME, 'input')
        pass_username.send_keys(login)
        pass_username.send_keys(Keys.ENTER)
        time.sleep(10)
        pass_password = driver.find_element(By.TAG_NAME, 'input')
        pass_password.send_keys(password)
        pass_password.send_keys(Keys.ENTER)

        # Send message:
        time.sleep(15)
        my_internet_message = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        my_internet_message.send_keys(self.internet_message)
        time.sleep(5)
        btn_send_twit = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span')
        btn_send_twit.click()

        driver.close()


internet = InternetSpeedTwitterBot()
internet.twitter_post(twitter_login, twitter_password)
