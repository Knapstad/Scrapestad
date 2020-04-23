from Page import Page
from Bot import Bot
from multiprocessing import Process, Queue, Manager
from threading import Thread
from queue import Empty
from workers import page_worker
import time
import traceback
import csv


if __name__ == "__main__":
    processes = 3
    manager= Manager()
    work_queue = Queue()
    worked_queue = Queue()
    tobeprocessed = manager.dict()
    isprocessed = manager.dict()
    workers=[]
    # with open("urls.csv", newline="") as file:
    #     reader = csv.reader(file)
    #     urls = [i[0] for i in reader if len(i)>0]
    urls=["http://example.com"]*200
    for i in urls:
        work_queue.put(i)
    work=[]
    for i in range(processes):
        p=Process(target=page_worker, args=(work_queue, worked_queue,tobeprocessed,isprocessed))
        work.append(p)
    start=time.time()
    for i in work:
        i.start()
    for i in work:
        i.join()
    end=time.time()
    print(f"took {end-start}")