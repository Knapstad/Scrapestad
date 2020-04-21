import asyncio
from pyppeteer import launch
import random
import time
import csv


async def get(urls):
    browser = await launch()
    
    while not urls.empty():
        try:
            url = urls.get_nowait()
            print("-----------------------")
            print(f"Getting url {url[1]}")
            print("-----------------------\n")
            page = await browser.newPage()
            await page.goto(url[0])
            element = await page.querySelector('title')
            title = await page.evaluate('(element) => element.textContent', element)
            # await asyncio.sleep(random.random())
            print("-----------------------")
            print(f"Return title: {title} of url {url[1]}")
            print("-----------------------\n")
            urls.task_done()
        except Exception as e:
            print(e)
            break    
    
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
    start = time.time()
    urls = await get_urls()
    await asyncio.gather(
        
        get(urls),
        get(urls),
        get(urls),
        get(urls),
        get(urls),
        get(urls),
        get(urls)
        
    )
    urls.join()
    print(f"____DONE____ in: ")
    print(f"{(time.time()-start)}")

# asyncio.run(main())
