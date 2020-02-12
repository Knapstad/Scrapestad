from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Page import Page
from Bot import Bot
from multiprocessing import Process, Queue, Manager
from threading import Thread
from queue import Queue as Koo
# import time



def page_worker(work_queue, worked_queue, behandleslist, erbehandlet):
    try:
        print(f"page worker start")
        bot = Bot()
        while True:
            url = work_queue.get()
            if url in erbehandlet:
                continue
            html = bot.get_html(url)
            page = Page(html)
            page.soup=None
            page.html=None
            worked_queue.put(page)
            erbehandlet.append(page.url)
            # erbehandlet.append(page.actual_url)
            negate = ["page=", "-jpeg", "pid=", "/calendar/createevent", "#", "-pdf"]
            for url in page.links:
                if url not in behandleslist and "www.obos.no" in url and not any(word in url for word in negate):
                    work_queue.put(url)
                    behandleslist.append(url)
            # print(f"\rIn work queue: {work_queue.qsize()}, In worked queue {worked_queue.qsize()}, er behandlet: {len(erbehandlet)}", end="")

    finally:
        bot.quit()

def table_worker(queue, table):
    while True:
        page=queue.get()
        currentRowCount = table.rowCount()
        table.setRowCount(currentRowCount + 1)
        table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
        table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
        table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
        table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
        table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
        table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
        table.setItem(currentRowCount, 6, QTableWidgetItem(f"{page.links}"))
        



def run_page_workers(first: str, num_workers: int, table):
    table=table
    manager= Manager()
    skalbehandles = Queue()
    erbehandletqueue = Queue()
    behandleslist = manager.list()
    erbehandlet = manager.list()
    workers=[]
    try:
        skalbehandles.put(first)
        for i in range(num_workers):
            print("starting process " + str(i))
            p = Process(target=page_worker, args=(skalbehandles,erbehandletqueue,behandleslist,erbehandlet))
            workers.append(p)
        for i in workers:
            i.start()
        tabwork = Thread(target=table_worker, args=(erbehandletqueue,table))
        tabwork.start()
        for i in workers:
            i.join()
    except Exception as e:
        print(e)

