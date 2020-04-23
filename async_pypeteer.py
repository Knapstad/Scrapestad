import asyncio
from pyppeteer import launch
import random
import time
import csv
import async_driver


async def get(urls: asyncio.Queue):
    browser = await launch()
    
    while not urls.empty():
        try:
            url = urls.get_nowait()
            # print("-----------------------")
            # print(f"Getting url {url[1]}")
            # print("-----------------------\n")
            page = await browser.newPage()
            await page.goto(url[0])
            element = await page.querySelector('title')
            title = await page.evaluate('(element) => element.textContent', element)
            # await asyncio.sleep(random.random())
            # print("-----------------------")
            # print(f"Return title: {title} of url {url[1]}")
            # print("-----------------------\n")
            urls.task_done()
        except Exception as e:
            print(e)
            break    
    
    await browser.close()
    