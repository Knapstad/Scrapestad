from selenium import webdriver


class Bot:
    ID = 0

    def __init__(self):
        Bot.ID += 1
        self.ID = Bot.ID
        self.driver = self.load_driver()

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
        self.driver.get(url)
        html = self.driver.page_source
        actual_url = self.driver.current_url
        return (url, html, actual_url)

    def quit(self):
        # print(f"quiting driver {self.ID}")
        self.driver.quit()
