from bs4 import BeautilfulSoup as BS

class Page():

    __init__(self, html: String):
        self.html = html

    def parse_html(self):
        soup = BS(html, "lxml")
        self.soup = soup

