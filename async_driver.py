import asyncio

from arsenic import get_session, browsers, services
import random

async def get(urls):
    service = services.Chromedriver(binary="C://Users/knaben/Documents/Scripts/Python/scraper/chromedriver.exe")
    browser = browsers.Chrome(chromeOptions={'args': ['--headless', '--disable-gpu', '--silent']})
    while not urls.empty():
        try:
            url = urls.get_nowait()
            async with get_session(service, browser) as session:
                await session.get(url[0])
        
                title = await session.get_element("title")
                title = await title.get_text()
            urls.task_done()
        except Exception as e:
            print(e)
            break  


