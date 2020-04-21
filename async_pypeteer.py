import asyncio
from pyppeteer import launch
import random
import time
import csv


async def get(urls):
    browser = await launch()
    start = time.time()
    while True:
        url = await urls.get()
        print(f"getting url {url[1]}")
        page = await browser.newPage()
        await page.goto(url[0])
        element = await page.querySelector('title')
        title = await page.evaluate('(element) => element.textContent', element)
        await asyncio.sleep(random.random())
        print(f"{title} of {url[1]}")
        urls.task_done()    
    print(f"{(time.time()-start)*1000}")
    await browser.close()

async def get_urls():
    with open("urls.csv", newline="") as file:
        reader = csv.reader(file)
        urls = asyncio.Queue()
        for i, j in enumerate(reader):
            if len(j)>0:
                await urls.put((j[0],i))
            if i > 20:
                break
        return urls

async def main():
    urls = await get_urls()
    await asyncio.gather(
        
        get(urls),
        get(urls),
        get(urls),
        get(urls),
        get(urls),
        get(urls)
        
    )
    urls.join()

asyncio.run(main())
