import os
from pathlib import Path

from selenium.webdriver import Chrome, Firefox, Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SponsorlytixDriver:

    def __init__(self, config, crawler_name='Social Media Crawler', browser=None):
        self.crawler_name = crawler_name
        self.config = config
        available_drivers = {
            'CHROME': self.__get_chrome_driver,
            'FIREFOX': self.__get_firefox_driver,
            'REMOTE': self.__get_remote_driver
        }
        driver_browser = browser.upper() if browser else self.config('browser', 'REMOTE')
        self.driver = available_drivers.get(driver_browser)()
        self.wait = WebDriverWait(self.driver, 5)

    def __get_remote_driver(self):
        driver_host = self.config.driver_host
        driver_user = self.config.driver_user
        driver_password = self.config.driver_password

        driver_remote_url = f"http://{driver_user}:{driver_password}@{driver_host}:4444/wd/hub"

        capabilities = dict()
        capabilities['zal:name'] = self.crawler_name
        capabilities['browserName'] = 'chrome'
        capabilities['zal:version'] = '88'
        capabilities['zal:platform'] = 'Linux'
        capabilities['zal:screenResolution'] = '1920x1080'
        capabilities['zal:record_video'] = 'true'
        capabilities['zal:record_network'] = 'false'

        return Remote(
            desired_capabilities=capabilities,
            command_executor=driver_remote_url)

    def __get_chrome_driver(self):
        options = Options()
        DRIVER_PATH = str(Path("chromedriver").resolve())
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("--disable-gpu")
        return Chrome(executable_path=DRIVER_PATH, options=options)

    def __get_firefox_driver(self):
        driver_dir = os.environ.get('FIREFOX_DRIVER') 
        return Firefox(executable_path=driver_dir)
 
    def quit(self):
        self.driver.quit()

    def find_element(self, element, wait_until=5, parent_element=None):
        '''
            Find Element

            Global finder for the most commons finders type of selenium (XPATH, ID, CLASS and NAME)

            Parameters:
            element (string): Element to find. / = XPATH # = ID . = CLASS

            wait_until (int): seconds to wait the element appears

            parent_element (selenium_element): Find the child of this element

            Returns:
            selenium_element
        '''
        driver = self.driver
        if parent_element:
            driver = parent_element

        find_by = {
            '/': {
                'wait_by': By.XPATH,
                'function': driver.find_element_by_xpath,
            },
            '#': {
                'wait_by': By.ID,
                'function': lambda elm: driver.find_element_by_id(elm[1:]),
            },
            '.': {
                'wait_by': By.CSS_SELECTOR,
                'function': lambda elm : driver.find_element_by_class_name(elm[1:]),
            }
        }

        element_initital = element[0]
        finder = find_by.get(element_initital)

        if finder:
            if wait_until and not parent_element:
                self.wait.until(EC.visibility_of_element_located((finder.get('wait_by'), element)))
            return finder.get('function')(element)

        return driver.find_element_by_name(element)
        