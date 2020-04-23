import PyPDF2 as pdf
import textract
import scholarly
# import refextract
import pdftitle
import webbrowser
import time
import notify2
import sys
import random

# from PySide2.QtCore import *
# from PySide2.QtGui import *
from PySide2.QtWidgets import (QWidget,QTabWidget,QVBoxLayout,QApplication)
# from PySide2.QtCharts import *
# from PySide2 import *
from PapersWindow import *
import Index

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # self.items = 0

        self.tabs = QTabWidget()
        self.papersTab= PapersTab()
        self.tabs.addTab(self.papersTab,"Papers")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    Index.load_json()
    print(Index.gPapers)
    notify2.init("PdfDB")

    app = QApplication([])

    widget = MainWindow()
    widget.resize(1600, 1000)
    widget.show()

    sys.exit(app.exec_())