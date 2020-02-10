from Page import Page
from Bot import Bot
from threading import Thread
from queue import Queue
# import time



def worker(queue):
    
    try:
        bot = Bot()
        while True:
            url = queue.get()
            print(url)
            html = bot.get_html(url)
            page = Page(html)
            erbehandlet.append(page)
            for i in page.links:
                if i not in behandleslist and"obos.no" in i:
                    queue.put(i)
                    behandleslist.append(i)
                if len(erbehandlet) >=10:
                    
                    return 
           
            # a.task_done()
    finally:

        bot.quit()

def run_page_workers(first: str, num_workers: int):
    skalbehandles = Queue()
    behandleslist = []
    erbehandlet = []
    try:
        skalbehandles.put(first)
        for i in range(4):
            p = Thread(target=worker, args=(skalbehandles,))
            p.start()
    
    except Exception as e:
        print(e)
