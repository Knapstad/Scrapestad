from Page import Page
from Bot import Bot


bot = Bot()
html = bot.get_html("https://www.obos.no")
page = Page(html[1], html[0])
page.make_soup()
page.get_meta()
page.get_images()

for i in page.images:
    print(i)
