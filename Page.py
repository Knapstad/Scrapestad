from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin


class Page:
    def __init__(self, html: tuple):
        self.html = html[1]
        self.url = html[0]
        self.actual_url = html[2]
        self.redirected = self.url not in self.actual_url
        self.description = ""
        self.meta_title = ""
        self.parse_html()
        self.set_meta()
        self.set_links(self.html)
        self.set_images()
        self.title = self.soup.find("title").text

    def __str__(self):
        representation = f"Url: {self.url}\nActual_url: {self.actual_url}\nIs redirected: {self.redirected}\nMeta_Description: {self.description}\nMeta_title: {self.meta_title}"
        return representation

    def __eq__(self, value):
        return value.actual_url == self.actual_url

    def __ne__(self, value):
        return not self == value

    def parse_html(self):
        soup = BS(self.html, "lxml")
        self.soup = soup

    def make_soup(self):
        soup = BS(self.html, "lxml")
        self.soup = soup

    def set_meta(self):
        metas = self.soup.findAll("meta")
        for i in metas:
            if i.get("name") == "description":
                self.description = i.get("content","")
            if i.get("name") == "title":
                self.meta_title = i.get("content","")

    def set_links(self, html):
        self.links = []
        soup = BS(html, "lxml")
        for link in soup.findAll("a"):
            if link.has_attr("href"):
                self.links.append(urljoin(self.actual_url, link["href"]))

    def get_links(self):
        if not self.links:
            self.set_links(self.html)
        return self.links

    def set_images(self):
        self.images = []
        imgs = self.soup.findAll("img")
        for i in imgs:
            self.images.append((urljoin(self.url, i.get("src")), i.get("alt","")))

    def get_images(self):
        if not self.images:
            set_images(self)
        return self.images

    def images_meta(self):
        self.images_missing_alt = []
        self.images_blank_alt = []
        self.images_with_alt = []
        for i in self.images:
            if i[1] == "":
                if i not in self.images_missing_alt:
                    self.images_missing_alt.append(i)
            elif i[1].isspace():
                if i not in self.images_blank_alt:
                    self.images_blank_alt.append(i)
            else:
                self.images_with_alt.append(i)

