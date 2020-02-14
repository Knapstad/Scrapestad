from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Page import Page
from Bot import Bot
from workers import table_worker, page_worker, run_page_workers
# from test import  
import typing

import time
import csv
import sys
import os




def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception as e:
            print(e)

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignRight|Qt.AlignCenter

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Knapstad -  OBOS")
        self.left = 500
        self.top = 500
        self.setWindowIcon(QIcon(resource_path("icon2.png")))
        self.threadpool = QThreadPool()

        def execute_add_data():
            antall.setText("Henter data...")
            worker = Worker(add_data, my_table)
            self.threadpool.start(worker)

        def get_one(table):
            with Bot() as bot:
                if not fragment.text().startswith("//"):
                    url = f"//{fragment.text()}"
                else:
                    url = fragment.text()
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
                

        def add_data(table):
            hent.setEnabled(False)
            if str(site.currentText()) == "alle":
                run_page_workers(fragment.text(),4,table,antall)

            if str(site.currentText()) == "en":
                get_one(table)
            hent.setEnabled(True)

        def lagre_data(table):
            try:
                header = ["Tittel", "Url","Actual url", "Redirected", "Description", "No. images", "Links"]
                filename = QFileDialog.getSaveFileName(
                    caption="Lagre fil",
                    directory=f"{fragment.text()}".lower(),
                    filter="Csv (*.csv)",
                )

                if filename[0]:
                    with open(filename[0], "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        for i in range(table.rowCount()):
                            writer.writerow([table.item(i,0).text(), table.item(i,1).text(), table.item(i,2).text(), table.item(i,3).text(), table.item(i,4).text(), table.item(i,5).text(), table.item(i,6).text()])
            except Exception as e:
                pritn(e)


        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()

        layout1.setContentsMargins(0, 0, 0, 0)
        layout2.setContentsMargins(30, 30, 40, 0)
        layout4.setContentsMargins(0, 0, 0, 0)
        layout5.setContentsMargins(0, 0, 0, 0)

        layout1.setSpacing(20)
        layout2.setSpacing(10)
        layout4.setSpacing(2)
        layout5.setSpacing(0)

        layout2.setAlignment(Qt.AlignVCenter)

        fragment_label = QLabel("Urlfragment:")
        fragment = QLineEdit("")
        fragment.returnPressed.connect(execute_add_data)
        fragment_width = (
            fragment_label.fontMetrics().boundingRect(fragment_label.text()).width()
        )
        fragment.setMaximumSize(200 - fragment_width, 20)

        my_table = QTableWidget()
        my_table.setColumnCount(10)
        my_table.setHorizontalHeaderLabels(["Tittel", "Url","Actual url", "Redirected", "Description", "images","images with alt", "images with blank alt", "images with no alt", "Links"])
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
        layout4.addWidget(fragment_label)
        layout4.addWidget(fragment)

        site_label = QLabel("Hvilken side:")
        site = QComboBox()
        site.addItems(["alle", "en"])
        layout5.addWidget(site_label)
        layout5.addWidget(site)

        hent = QPushButton("Hent urler")
        hent.setMaximumSize(200, 30)
        lagre = QPushButton("Lagre urler")
        lagre.setMaximumSize(200, 30)
        hent.clicked.connect(execute_add_data)
        lagre.clicked.connect(lambda: lagre_data(my_table))
        antall = QLabel("")

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(lambda: lagre_data(my_table))

        layout2.addLayout(layout5)
        layout2.addLayout(layout4)
        layout2.addWidget(hent)
        layout2.addWidget(lagre)
        layout2.addWidget(antall)
        layout1.addLayout(layout2)

        layout3.addWidget(my_table)

        layout1.addLayout(layout3)

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