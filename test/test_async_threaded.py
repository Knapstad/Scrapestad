import asyncio
from threading import Thread
from queue import Queue
import time
import async_test
import janus

from async_driver import get


def thr(urls):
    # we need to create a new loop for the thread, and set it as the 'default'
    # loop that will be returned by calls to asyncio.get_event_loop() from this
    # thread.
    loop = asyncio.new_event_loop()
    # print("loop set")
    asyncio.set_event_loop(loop)
    # print("loop assiged")
    asyncio.run(async_test.main2(4, urls))
    # print("loop run")
    # loop.close()


if __name__ == "__main__":


    urls = ["https://example.com"]*200
    urlqueue = Queue()
    for i, y in enumerate(urls):
        urlqueue.put((y,i))
    
    work=[]
    for i in range(10):
        t = Thread(target=thr, args=(urlqueue,))
        work.append(t)
    start=time.time()
    for i in work:
        i.start()
    for i in work:
        i.join()
    end=time.time()
    print(f"Execution took {end - start}")

