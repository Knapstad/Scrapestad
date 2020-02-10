from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Page import Page
from Bot import Bot
import time
import os
import sys
from test import *


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

        def get_all(urls, table):
            bot = Bot()
            for url in urls:
                if ".obos.no" in url and "mail" not in url and "tel" not in url and "#main" not in url:
                    try:
                        html=bot.get_html(url)
                        page = Page(html)
                        currentRowCount = table.rowCount()
                        table.setRowCount(currentRowCount + 1)
                        table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
                        table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
                        table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
                        table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
                        table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
                        table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
                        table.setItem(currentRowCount, 6, QTableWidgetItem(f"{page.links}"))
                        for i in page.get_links():
                            if i not in urls:
                                urls.append(i)
                        antall.setText(f"Antall urler: {len(urls)}")
                    except Exception as e:
                        print(e)
            bot.quit()

        def add_data(table):
            hent.setEnabled(False)
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(["Tittel", "Url","Actual url", "Redirected", "Description", "No. images", "Links"])
            table.setRowCount(0)
            table.setColumnWidth(0,200)
            table.setColumnWidth(1,300)
            table.setColumnWidth(2,300)
            table.setColumnWidth(3,100)
            table.setColumnWidth(4,500)
            table.setColumnWidth(5,60)
            table.setColumnWidth(6,500)

            if str(site.currentText()) == "alle":
                run_page_workers(fragment.text(),4,table)
                # bot = Bot()
                # html = bot.get_html(fragment.text())
                # page = Page(html)
                # currentRowCount = table.rowCount()
                # table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
                # table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
                # table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
                # table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
                # table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
                # table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
                # table.setItem(currentRowCount, 6, QTableWidgetItem(f"{page.links}"))
                # urls = page.get_links()
                # # for i in range(3):
                # for url in urls:
                #     if ".obos.no" in url and "mail" not in url and "tel" not in url and "#main" not in url:
                #         try:
                #             html=bot.get_html(url)
                #             page = Page(html)
                #             currentRowCount = table.rowCount()
                #             table.setRowCount(currentRowCount + 1)
                #             table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
                #             table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
                #             table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
                #             table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
                #             table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
                #             table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
                #             table.setItem(currentRowCount, 6, QTableWidgetItem(f"{page.links}"))
                #             for i in page.get_links():
                #                 if i not in urls:
                #                     urls.append(i)
                #             antall.setText(f"Antall urler: {len(urls)}")
                #         except Exception as e:
                #             print(e)

            if str(site.currentText()) == "en":
                bot = Bot()
                html = bot.get_html(fragment.text())
                page = Page(html)
                currentRowCount = table.rowCount()
                table.setItem(currentRowCount, 0, QTableWidgetItem(f"{page.title}"))
                table.setItem(currentRowCount, 1, QTableWidgetItem(f"{page.url}"))
                table.setItem(currentRowCount, 2, QTableWidgetItem(f"{page.actual_url}"))
                table.setItem(currentRowCount, 3, QTableWidgetItem(f"{page.redirected}"))
                table.setItem(currentRowCount, 4, QTableWidgetItem(f"{page.description}"))
                table.setItem(currentRowCount, 5, QTableWidgetItem(f"{len(page.images)}"))
                table.setItem(currentRowCount, 6, QTableWidgetItem(f"{page.links}"))
            bot.quit()
            hent.setEnabled(True)

        def lagre_data(table):
            try:
                data = "urls"
                for i in range(table.rowCount()):
                    data += f"\n{table.item(i,0).text()}"
                filename = QFileDialog.getSaveFileName(
                    caption="Lagre fil",
                    directory=f"{fragment.text()}".lower(),
                    filter="Csv (*.csv)",
                )

                if filename[0]:
                    with open(filename[0], "w") as f:
                        f.write(data)
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


app = QApplication(list(""))

window = MainWindow()
window.resize(1000, 500)
window.show()


# Start the event loop.
app.exec_()
