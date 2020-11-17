from windows.options import OptionsWindow
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
        self.options = OptionsWindow()

        self.layout1 = QHBoxLayout()
        self.left_sidebar = QVBoxLayout()
        self.table_layout = QVBoxLayout()
        self.fragment_layout = QHBoxLayout()
        self.site_layout = QHBoxLayout()
        self.crawl_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.menubar = self.menuBar()
        
        self.exit = QAction("Quit", self)
        self.exit.triggered.connect(sys.exit)
        self.optionsmenu = QAction("Options", self)
        self.optionsmenu.triggered.connect(self.options.show)
        
        self.fileMenu = self.menubar.addMenu("File")
        self.fileMenu.addAction(self.optionsmenu)
        self.fileMenu.addAction(self.exit)

        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.left_sidebar.setContentsMargins(30, 30, 40, 0)
        self.fragment_layout.setContentsMargins(0, 0, 0, 0)
        self.site_layout.setContentsMargins(0, 0, 0, 0)
        self.crawl_layout.setContentsMargins(0,0,0,25)
        self.table_layout.setContentsMargins(0,15,0,0)

        self.layout1.setSpacing(40)
        self.left_sidebar.setSpacing(10)
        self.fragment_layout.setSpacing(2)
        self.site_layout.setSpacing(0)
        self.crawl_layout.setSpacing(0)
        self.button_layout.setSpacing(0)

        self.left_sidebar.setAlignment(Qt.AlignVCenter)

        self.fragment_label = QLabel("Url:")
        self.fragment = QLineEdit("")
        self.fragment.returnPressed.connect(self.execute_add_data)
        fragment_width = (
            self.fragment_label.fontMetrics().boundingRect(self.fragment_label.text()).width()
        )
        self.fragment.setMaximumSize(200 - fragment_width, 20)

        self.crawl_label = QLabel("Crawl subdomains:")
        self.crawl_sub = QCheckBox()


        self.my_table = QTableWidget()
        self.my_table.setColumnCount(10)
        self.my_table.setHorizontalHeaderLabels(["Title", "Url","Actual url", "Redirected", "Description", "Images","Images with alt", "Images with blank alt", "Images with no alt", "Links"])
        self.my_table.resizeColumnsToContents()
        self.my_table.setRowCount(0)
        self.my_table.setColumnWidth(0,200)
        self.my_table.setColumnWidth(1,250)
        self.my_table.setColumnWidth(2,250)
        self.my_table.setColumnWidth(4,300)
        self.my_table.setColumnWidth(9,500)
        delegate = AlignDelegate(self.my_table)
        self.my_table.setItemDelegateForColumn(5, delegate)
        self.my_table.setItemDelegateForColumn(6, delegate)
        self.my_table.setItemDelegateForColumn(7, delegate)
        self.my_table.setItemDelegateForColumn(8, delegate)
        
        self.fragment_label.setMaximumSize(fragment_width + 5, 20)
        self.fragment_layout.addWidget(self.fragment_label)
        self.fragment_layout.addWidget(self.fragment)

        self.site_label = QLabel("Hvilken side:")
        self.site = QComboBox()
        self.site.addItems(["alle", "en"])
        self.site_layout.addWidget(self.site_label)
        self.site_layout.addWidget(self.site)

        self.crawl_layout.addWidget(self.crawl_label)
        self.crawl_layout.addWidget(self.crawl_sub)

        self.hent = QPushButton("Hent urler")
        self.hent.setMaximumSize(200, 30)
        self.lagre = QPushButton("Lagre urler")
        self.lagre.setMaximumSize(200, 30)
        self.optionsbutton = QPushButton("settings")
        self.optionsbutton.setMaximumSize(200, 30)
        self.optionsbutton.clicked.connect(self.options.show)
        self.hent.clicked.connect(self.execute_add_data)
        self.lagre.clicked.connect(lambda: save_data(self.my_table))
        self.antall = QLabel("")


        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(lambda: save_data(self.my_table))

        self.button_layout.addWidget(self.hent)
        self.button_layout.addWidget(self.lagre)
        self.button_layout.addWidget(self.optionsbutton)
        self.button_layout.addWidget(self.antall)

        self.left_sidebar.addLayout(self.site_layout)
        self.left_sidebar.addLayout(self.fragment_layout)
        self.left_sidebar.addLayout(self.crawl_layout)
        self.left_sidebar.addLayout(self.button_layout)
        self.layout1.addLayout(self.left_sidebar)

        self.table_layout.addWidget(self.my_table)

        self.layout1.addLayout(self.table_layout)
        # self.layout1.addLayout(fileMenu)

        self.widget = QWidget()
        self.widget.setLayout(self.layout1)
        self.setCentralWidget(self.widget)

    def execute_add_data(self):
        if not RUNNING.value :
            # print(f"Active: {bool(ACTIVE)} and running: {bool(RUNNING)} ")
            self.antall.setText("Henter data...")
            worker = Worker(self.add_data, self.my_table, ACTIVE)
            RUNNING.value = 1
            self.hent.setText("Pause")
            
            self.threadpool.start(worker)
        elif ACTIVE.value and RUNNING.value:
            # print(f"Active: {bool(ACTIVE.value)} and running: {bool(RUNNING.value)} ")
            ACTIVE.value = 0
            self.hent.setText("Resume")
        elif not ACTIVE.value and RUNNING.value:
            # print(f"Active: {bool(ACTIVE.value)} and running: {bool(RUNNING.value)} ")
            # print(ACTIVE.value)
            ACTIVE.value = 1
            self.hent.setText("Pause")

    def get_one(table: QTableWidget, url: str):
        with Bot() as bot:
            html = bot.get_html(url)
            page = Page(html)
            self.currentRowCount = table.rowCount()
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
            self.antall.setText(f"Antall urler: 1")


    def add_data(self, table , run):
        domain = tldextract.extract(self.fragment.text())

        if self.crawl_sub.isChecked():
            set_config("domain", ".".join(domain[1:]))
        else:
            set_config("domain", ".".join(domain))

        if str(self.site.currentText()) == "alle":
            run_page_workers(self.fragment.text(), 5, table, self.antall, run)

        if str(self.site.currentText()) == "en":
            get_one(table, self.fragment.text())
        self.hent.setText("Fetch Urls")
        

    def save_data(self, table):
        try:
            header = ["Tittel", "Url","Actual url", "Redirected", "Description", "Images","Images with alt", "Images with blank alt", "Images with no alt", "Links"]
            filename = QFileDialog.getSaveFileName(
                caption="Lagre fil",
                directory=f"{self.fragment.text()}".replace(".","-").lower(),
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



if __name__ == "__main__":
    app = QApplication(list(""))

    window = MainWindow()
    window.showMaximized()
    window.show()


    # Start the event loop.
    app.exec_()