import sys
import os
print(f"Wd: {os.getcwd()}")
if "windows" in os.getcwd():
    sys.path.insert(1,'..')
else:
    sys.path.insert(1,'.')

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from config.config import config, set_config

import sys

class OptionsWindow(QWidget):


    def __init__(self):
        super().__init__()
        ignore = QTextEdit()
        ignore.setText(", ".join(config["negate"]))
        ignore.setFixedHeight(50)
        cancel = QPushButton("Cancel")
        cancel.setMaximumWidth(200)
        save = QPushButton("Save")
        save.clicked.connect(lambda: self.save_settings(ignore))
        layout = QFormLayout()
        layout.addRow(QLabel("Respect robots.txt:"),QCheckBox())
        layout.addRow(QLabel("Ignore urls with:"),ignore)
        layout.addRow(save,cancel)
        self.setLayout(layout) 

    def save_settings(self, ignore):
        set_config("negate", ignore.toPlainText().split(","))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = OptionsWindow()
    dialog.show()
    app.exec_()