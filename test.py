from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Page import Page
from Bot import Bot
from threading import Thread
from queue import Queue
# import time



def page_worker(work_queue, worked_queue, behandleslist, erbehandlet):
    try:
        bot = Bot()
        while True:
            url = work_queue.get()
            html = bot.get_html(url)
            page = Page(html)
            worked_queue.put(page)
            erbehandlet.append(page)
            for url in page.links:
                if url not in behandleslist and "www.obos.no" in url and "#main" not in url and "page=" not in url:
                    work_queue.put(url)
                    behandleslist.append(url)
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
    skalbehandles = Queue()
    erbehandletqueue = Queue()
    behandleslist = []
    erbehandlet = []
    try:
        skalbehandles.put(first)
        for i in range(4):
            p = Thread(target=page_worker, args=(skalbehandles,erbehandletqueue,behandleslist,erbehandlet))
            p.start()
        tabwork = Thread(target=table_worker, args=(erbehandletqueue,table))
        tabwork.start()
    except Exception as e:
        print(e)

