import asyncio

from arsenic import get_session, browsers, services
import random

async def get(url):
    service = services.Chromedriver(binary="C://Users/knaben/Documents/Scripts/Python/scraper/chromedriver.exe")
    browser = browsers.Chrome(chromeOptions={'args': ['--headless', '--disable-gpu', '--silent']})
    async with get_session(service, browser) as session:
        await session.get(url)
        await asyncio.sleep(random.randint(1,2))
        title = await session.get_element("title")
        title = await title.get_text()
        print(title)
        print("im done")

asyncio.run(get("https://www.obos.no"))
