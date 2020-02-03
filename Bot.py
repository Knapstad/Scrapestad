from selenium import Webdriver


class Bot():

    def __init__(self):


    def load_driver(self, headless=True):
        """Opens a webdriver instance with chromedriver
                
        Returns:
        Webdriver  -- The webdriver instance
        """

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("user-agent=Obosbot")
        driver = webdriver.Chrome(
            executable_path=r"chromedriver.exe",
            options=options,
        )
        return driver
