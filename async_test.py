
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
async def get_example_urls(number: int):
    urls = asyncio.Queue()
    for i in range(number):
        await urls.put(("https://example.com",i))
    return urls

async def main(workers, drivers = None):
    # get=async_driver.get
    
    start = time.time()
    urls = await get_example_urls(200)
    tasks = (get(urls) for i in range(workers))
    await asyncio.gather(*tasks)
    # await asyncio.gather(
        
    #     [get(urls),
    #     get(urls),
    #     get(urls),
    #     get(urls),
    #     get(urls),
    #     get(urls),
    #     get(urls)]
        
    # )
    await urls.join()
    print(f"____DONE____ in: ")
    print(f"{(time.time()-start)}")
    print(f"With {workers} workers")

# asyncio.run(main(3))
# asyncio.run(main(5))
# asyncio.run(main(10))
asyncio.run(main(3))