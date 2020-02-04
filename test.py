from Page import Page
from Bot import Bot


bot = Bot()
html = bot.get_html("https://www.vg.no")
page = Page(html[0], html[1], html[2])
page.make_soup()
page.set_meta()
page.set_images()

print(page)