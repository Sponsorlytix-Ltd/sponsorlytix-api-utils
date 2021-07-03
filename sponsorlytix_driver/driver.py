from pathlib import Path
from selenium import webdriver

from selenium.webdriver import Remote, Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SponsorlytixDriver:

    def __init__(self, config ,crawler_name='Social Media Crawler'):
        self.crawler_name = crawler_name
        self.config = config
        if self.config.driver_remote:
            self.driver = self.__get_remote_driver()
        else:
            self.driver = self.__get_web_driver()
        self.wait = WebDriverWait(self.driver, self.config.timeout)

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

    def __get_web_driver(self):
        options = Options()
        DRIVER_PATH = str(Path("chromedriver").resolve())
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("--disable-gpu")
        options.binary_location = DRIVER_PATH
        return Chrome(executable_path=DRIVER_PATH, options=options)

    def quit(self):
        self.driver.quit()

    def find_element(self, element, wait_until=2, parent_element=None):
        '''
            Find Element

            Global finder for the most commons finders type of selenium (XPATH, ID, CLASS and NAME)

            Parameters:
            element (string): Element to find.
                              / = XPATH
                              # = ID
                              . = CLASS

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
                'type': By.ID,
                'function': driver.find_element_by_id,
            },
            '.': {
                'type': By.CLASS_NAME,
                'function': driver.find_element_by_class_name,
            }
        }

        element_initital = element[0]
        finder = find_by.get(element_initital)

        if finder:
            if wait_until and not parent_element:
                self.wait.until(EC.visibility_of_element_located(By.XPATH, element))
            return finder.get('function')(element)

        return driver.find_element_by_name(element)
        