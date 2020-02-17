from selenium import webdriver
from urllib.parse import urlparse

class Bot:
    ID = 0

    def __init__(self):
        Bot.ID += 1
        self.ID = Bot.ID
        self.driver = self.load_driver()

    def __enter__(self): 
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.driver.quit()


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
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument("--silent")
            options.add_argument("user-agent=Obosbot")
            driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
            # print(f"driver {self.ID} loaded")
            return driver

    def get_html(self, url) -> tuple:
        if not url.startswith("//") and not url.startswith("http"):
            url = f"//{url}"
        self.url = urlparse(url,scheme="https")
        self.driver.get(self.url.geturl())
        html = self.driver.page_source
        actual_url = self.driver.current_url
        return (self.url.geturl(), html, actual_url)

    def quit(self):
        # print(f"quiting driver {self.ID}")
        self.driver.quit()
