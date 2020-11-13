from re import A
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Page import Page
from Bot import Bot
from workers import run_page_workers, Worker
from config.config import set_config
from multiprocessing import Value

from urllib.parse import urlparse
import tldextract

import typing
import config
import time
import csv
import sys
import os


RUNNING = Value("i",0)
ACTIVE = Value("i",1)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignRight|Qt.AlignCenter

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Scrapestad SEOscraper")
        self.left = 500
        self.top = 500
        self.setWindowIcon(QIcon(resource_path("icon2.png")))
        self.threadpool = QThreadPool()

        def execute_add_data():
            if not RUNNING.value :
                # print(f"Active: {bool(ACTIVE)} and running: {bool(RUNNING)} ")
                antall.setText("Henter data...")
                worker = Worker(add_data, my_table, ACTIVE)
                RUNNING.value = 1
                hent.setText("Pause")
                
                self.threadpool.start(worker)
            elif ACTIVE.value and RUNNING.value:
                # print(f"Active: {bool(ACTIVE.value)} and running: {bool(RUNNING.value)} ")
                ACTIVE.value = 0
                hent.setText("Resume")
            elif not ACTIVE.value and RUNNING.value:
                # print(f"Active: {bool(ACTIVE.value)} and running: {bool(RUNNING.value)} ")
                # print(ACTIVE.value)
                ACTIVE.value = 1
                hent.setText("Pause")
            

        def get_one(table: QTableWidget, url: str):
            with Bot() as bot:
                html = bot.get_html(url)
                page = Page(html)
                currentRowCount = table.rowCount()
                table.setRowCount(currentRowCount + 1)
                table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
                table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
                table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
                table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
                table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
                table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
                table.setItem(currentRowCount, 6, QTableWidgetItem(f"{len(page.images_with_alt)}"))
                table.setItem(currentRowCount, 7, QTableWidgetItem(f"{len(page.images_blank_alt)}"))
                table.setItem(currentRowCount, 8, QTableWidgetItem(f"{len(page.images_missing_alt)}"))
                table.setItem(currentRowCount, 9, QTableWidgetItem(f"{page.links}"))
                antall.setText(f"Antall urler: 1")
                

        def add_data(table , run):
            domain = tldextract.extract(fragment.text())

            if crawl_sub.isChecked():
                set_config("domain", ".".join(domain[1:]))
            else:
                set_config("domain", ".".join(domain))

            if str(site.currentText()) == "alle":
                run_page_workers(fragment.text(), 5, table, antall, run)

            if str(site.currentText()) == "en":
                get_one(table, fragment.text())
            hent.setText("Fetch Urls")
            

        def lagre_data(table):
            try:
                header = ["Tittel", "Url","Actual url", "Redirected", "Description", "Images","Images with alt", "Images with blank alt", "Images with no alt", "Links"]
                filename = QFileDialog.getSaveFileName(
                    caption="Lagre fil",
                    directory=f"{fragment.text()}".replace(".","-").lower(),
                    filter="Csv (*.csv)",
                )

                if filename[0]:
                    with open(filename[0], "w", newline="", encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        for row in range(table.rowCount()):
                            data=[]
                            for column in range(table.columnCount()):
                                data.append(table.item(row,column).text())
                            try:
                                writer.writerow(data)
                            except Exception as e:
                                print(f"could not write {data} -- {e}")
            except Exception as e:
                print(e)


        layout1 = QHBoxLayout()
        left_sidebar = QVBoxLayout()
        table_layout = QVBoxLayout()
        fragment_layout = QHBoxLayout()
        site_layout = QHBoxLayout()
        crawl_layout = QHBoxLayout()
        button_layout = QVBoxLayout()
        menubar = self.menuBar()
        
        exit = QAction("Quit",self)
        exit.triggered.connect(sys.exit)
        
        
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction("Options")
        fileMenu.addAction(exit)

        layout1.setContentsMargins(0, 0, 0, 0)
        left_sidebar.setContentsMargins(30, 30, 40, 0)
        fragment_layout.setContentsMargins(0, 0, 0, 0)
        site_layout.setContentsMargins(0, 0, 0, 0)
        crawl_layout.setContentsMargins(0,0,0,25)
        table_layout.setContentsMargins(0,15,0,0)

        layout1.setSpacing(40)
        left_sidebar.setSpacing(10)
        fragment_layout.setSpacing(2)
        site_layout.setSpacing(0)
        crawl_layout.setSpacing(0)
        button_layout.setSpacing(0)

        left_sidebar.setAlignment(Qt.AlignVCenter)

        fragment_label = QLabel("Url:")
        fragment = QLineEdit("")
        fragment.returnPressed.connect(execute_add_data)
        fragment_width = (
            fragment_label.fontMetrics().boundingRect(fragment_label.text()).width()
        )
        fragment.setMaximumSize(200 - fragment_width, 20)

        crawl_label = QLabel("Crawl subdomains:")
        crawl_sub = QCheckBox()


        my_table = QTableWidget()
        my_table.setColumnCount(10)
        my_table.setHorizontalHeaderLabels(["Title", "Url","Actual url", "Redirected", "Description", "Images","Images with alt", "Images with blank alt", "Images with no alt", "Links"])
        my_table.resizeColumnsToContents()
        my_table.setRowCount(0)
        my_table.setColumnWidth(0,200)
        my_table.setColumnWidth(1,250)
        my_table.setColumnWidth(2,250)
        my_table.setColumnWidth(4,300)
        my_table.setColumnWidth(9,500)
        delegate = AlignDelegate(my_table)
        my_table.setItemDelegateForColumn(5, delegate)
        my_table.setItemDelegateForColumn(6, delegate)
        my_table.setItemDelegateForColumn(7, delegate)
        my_table.setItemDelegateForColumn(8, delegate)
        
        fragment_label.setMaximumSize(fragment_width + 5, 20)
        fragment_layout.addWidget(fragment_label)
        fragment_layout.addWidget(fragment)

        site_label = QLabel("Hvilken side:")
        site = QComboBox()
        site.addItems(["alle", "en"])
        site_layout.addWidget(site_label)
        site_layout.addWidget(site)

        crawl_layout.addWidget(crawl_label)
        crawl_layout.addWidget(crawl_sub)

        hent = QPushButton("Hent urler")
        hent.setMaximumSize(200, 30)
        lagre = QPushButton("Lagre urler")
        lagre.setMaximumSize(200, 30)
        hent.clicked.connect(execute_add_data)
        lagre.clicked.connect(lambda: lagre_data(my_table))
        antall = QLabel("")


        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(lambda: lagre_data(my_table))

        button_layout.addWidget(hent)
        button_layout.addWidget(lagre)
        button_layout.addWidget(antall)

        left_sidebar.addLayout(site_layout)
        left_sidebar.addLayout(fragment_layout)
        left_sidebar.addLayout(crawl_layout)
        left_sidebar.addLayout(button_layout)
        layout1.addLayout(left_sidebar)

        table_layout.addWidget(my_table)

        layout1.addLayout(table_layout)
        # layout1.addLayout(fileMenu)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(list(""))

    window = MainWindow()
    window.showMaximized()
    window.show()


    # Start the event loop.
    app.exec_()