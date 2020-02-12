from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Page import Page
from Bot import Bot
from multiprocessing import Process, Queue, Manager
from threading import Thread
from queue import Empty
import time
import traceback



def page_worker(work_queue, worked_queue, behandleslist, erbehandlet):
    empty=0
    try:
        print(f"page worker start")
        bot = Bot()
        while True:
            if len(erbehandlet) > 30:
                break
            try:
                url = work_queue.get(timeout=1)
            except Empty:
                empty+=1
                time.sleep(2)
                if empty >= 3:
                    return
                continue
            if url in erbehandlet:
                continue
            html = bot.get_html(url)
            page = Page(html)
            page.soup=None
            page.html=None
            worked_queue.put(page)
            erbehandlet[page.url]=1
            erbehandlet[page.actual_url]=1
            # erbehandlet.append(page.actual_url)
            negate = ["page=", "-jpeg", "pid=", "/calendar/createevent", "#", "-pdf"]
            for url in page.links:
                if url not in behandleslist and "www.obos.no" in url and not any(word in url for word in negate):
                    work_queue.put(url)
                    behandleslist[url]=1
            print(f"\rIn work queue: {work_queue.qsize()}, In worked queue {worked_queue.qsize()}, er behandlet: {len(erbehandlet)}", end="")

    finally:
        bot.quit()
        worked_queue.put("done")
        print("Pageworker done")

def table_worker(queue, table, num_workers):
    num_workers=num_workers
    done=0
    print("I am TableWorker!!")
    while True:
        try:
            page=queue.get(timeout=2)
            if page == "done":
                done+=1
                if done >= num_workers:
                    print("done")
                    return
                continue

            currentRowCount = table.rowCount()
            table.setRowCount(currentRowCount + 1)
            # print("Setting title")
            table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
            # print("Setting url")
            table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
            # print("Setting url2")
            table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
            # print("Setting redir")
            table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
            # print("Setting desc")
            table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
            # print("Setting img")
            table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
            # print("Setting links")
            table.setItem(currentRowCount, 6, QTableWidgetItem(f"{page.links}"))
        except Empty:
                continue
        except Exception as E:
            traceback.print_exc()


def run_page_workers(first: str, num_workers: int, table):
    table=table
    manager= Manager()
    skalbehandles = Queue()
    erbehandletqueue = Queue()
    behandleslist = manager.dict()
    erbehandlet = manager.dict()
    workers=[]
    try:
        skalbehandles.put(first)
        for i in range(num_workers):
            print("starting process " + str(i))
            p = Process(target=page_worker, args=(skalbehandles, erbehandletqueue, behandleslist, erbehandlet))
            p.daemon = True
            workers.append(p)
        for i in workers:
            i.start()
        tabwork = Thread(target=table_worker, args=(erbehandletqueue, table, num_workers))
        tabwork.start()
        for i in workers:
            print(f"joining {i}")
            i.join()
    except Exception as e:
        print(e)

