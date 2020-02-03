from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin


class Page:
    def __init__(self, html: str, url: str):
        self.html = html
        self.url = url

    def parse_html(self):
        soup = BS(self.html, "lxml")
        self.soup = soup

    def make_soup(self):
        soup = BS(self.html, "lxml")
        self.soup = soup

    def get_meta(self):
        metas = self.soup.findAll("meta")
        for i in metas:
            # print(i)
            # print(f'{i.get("name")} {i.get("content")}')
            if i.get("name") == "description":
                self.description = i.get("content")
            if i.get("name") == "title":
                self.meta_title = i.get("content")

    def get_links(self, html):
        self.links = []
        soup = BS(html, "lxml")
        for link in soup.findAll("a"):
            if link.has_attr("href"):
                self.links.append(urljoin("https://www.obos.no", link["href"]))

    def return_links(self):
        if not self.links:
            self.get_links(self.html)
        return self.links

    def get_images(self):
        self.images = []
        imgs = self.soup.findAll("img")
        for i in imgs:
            self.images.append((urljoin(self.url, i.get("src")), i.get("alt")))
