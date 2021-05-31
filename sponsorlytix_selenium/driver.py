from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from config import get_config


configs = get_config()


class SponsorlytixDriver:

    def __init__(self, crawler_name='Social Media Crawler'):
        self.crawler_name = crawler_name
        if configs.driver_remote:
            self.driver = self.__get_remote_driver()
        else:
            self.driver = self.__get_web_driver()
        self.wait = WebDriverWait(self.driver, configs.timeout)

    def __get_remote_driver(self):
        driver_host = "3.16.155.212"
        driver_user = "sponsorlytix"
        driver_password = "HXMswfgn7E7Y"

        driver_remote_url = f"http://{driver_user}:{driver_password}@{driver_host}:4444/wd/hub"

        capabilities = dict()
        capabilities['zal:name'] = self.crawler_name
        capabilities['browserName'] = 'chrome'
        capabilities['zal:version'] = '88'
        capabilities['zal:platform'] = 'Linux'
        capabilities['zal:screenResolution'] = '1920x1080'
        capabilities['zal:record_video'] = 'true'
        capabilities['zal:record_network'] = 'false'

        return webdriver.Remote(
            desired_capabilities=capabilities,
            command_executor=driver_remote_url)

    def __get_web_driver(self):
        options = Options()
        DRIVER_PATH = str(Path("chromedriver").resolve())
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("--disable-gpu")
        options.binary_location = DRIVER_PATH
        return webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    def quit(self):
        self.driver.quit()
