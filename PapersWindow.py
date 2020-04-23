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
# import popplerqt5
import subprocess
from PySide2.QtCore import Qt,Slot
from PySide2.QtGui import (QImage,QPixmap)
from PySide2.QtWidgets import (QLineEdit,QInputDialog,QPushButton,QLabel,QWidget,QTableWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QAction)
# from PySide2.QtCharts import *
# from PySide2 import *

import Index

class PapersTab(QWidget):
	def __init__(self):
		right_width = 400

		QWidget.__init__(self)
        # self.items = 0

		self.selected_paper_index = -1

		self.table = QTableWidget()
		self.table.setColumnCount(5)
		self.table.setHorizontalHeaderLabels(['Title', 'Authors', 'Tags', 'Name', 'Abstract'])
		self.table.horizontalHeader().setSectionsMovable(True)
		self.table.setColumnWidth(0, 300)
		self.table.setColumnWidth(1, 200)
		self.table.setColumnWidth(2, 200)
		self.table.setColumnWidth(3, 400)

		self.table.setRowCount(len(Index.gPapers))
		self.table.setSortingEnabled(True)
		
		# self.document = popplerqt5.Poppler.Document.load(Index.gPapers[0]['path'])
		# self.page = self.document.page(0)
		# self.image = self.page.renderToImage(0, 0, 0, 0)
		# self.preview = QLabel('')
		# self.preview.setPixmap(QPixmap.fromImage(self.image))

		# print(Index.gPapers)

		i = 0
		for paper in Index.gPapers:
			print(paper)
			item1 = QTableWidgetItem()
			self.table.setItem(i, 0, item1)
			item1.setText(paper['title'])
			item1.setFlags(Qt.ItemIsEnabled)

			authors=''
			if 'authors' in paper:
				authors = paper['authors']
			item2 = QTableWidgetItem()
			self.table.setItem(i, 1, item2)
			item2.setText(authors)
			item2.setFlags(Qt.ItemIsEnabled)

			tags=[]
			if 'tags' in paper:
				tags = paper['tags']
			item3 = QTableWidgetItem()
			self.table.setItem(i, 2, item3)
			item3.setText(str(tags))
			item3.setFlags(Qt.ItemIsEnabled)

			item4 = QTableWidgetItem()
			self.table.setItem(i, 3, item4)
			item4.setText(paper['path'])
			item4.setFlags(Qt.ItemIsEnabled)

			abstract=''
			if 'abstract' in paper:
				abstract = paper['abstract']
			item5 = QTableWidgetItem()
			self.table.setItem(i, 4, item5)
			item5.setText(abstract)
			item5.setFlags(Qt.ItemIsEnabled)
			i+=1

		self.paper_title = QLabel('')
		self.paper_title.setFixedWidth(right_width)
		self.paper_title.setWordWrap(True)
		self.paper_authors = QLabel('')
		self.paper_authors.setFixedWidth(right_width)
		self.paper_authors.setWordWrap(True)
		self.paper_tags = QLabel('')
		self.paper_tags.setFixedWidth(right_width)
		self.paper_tags.setWordWrap(True)
		self.paper_filename = QLabel('')
		self.paper_filename.setFixedWidth(right_width)
		self.paper_filename.setWordWrap(True)
		self.paper_abstract = QLabel('')
		self.paper_abstract.setFixedWidth(right_width)
		self.paper_abstract.setWordWrap(True)

		self.right = QVBoxLayout()
		self.right.addWidget(self.paper_title)
		self.right.addWidget(self.paper_authors)
		self.right.addWidget(self.paper_tags)
		self.right.addWidget(self.paper_filename)
		self.right.addWidget(self.paper_abstract)

		self.url_button = QPushButton('Link')
		self.google_button = QPushButton('Google')
		self.scholar_button = QPushButton('Scholar')
		self.citations_button = QPushButton('Citations')
		self.reindex_button = QPushButton('Reindex')

		self.buttons = QHBoxLayout()
		self.buttons.addWidget(self.url_button)
		self.buttons.addWidget(self.scholar_button)
		self.buttons.addWidget(self.google_button)
		self.buttons.addWidget(self.citations_button)
		self.buttons.addWidget(self.reindex_button)

		self.right.addLayout(self.buttons)
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.table)
		self.layout.addLayout(self.right)

		self.setLayout(self.layout)

		# doubleclick_action = QAction("cellDoubleClicked", self)
		self.table.cellDoubleClicked.connect(self.cell_double_click)
		self.table.cellClicked.connect(self.cell_click)

		self.url_button.clicked.connect(self.url_button_click)
		self.google_button.clicked.connect(self.google_button_click)
		self.scholar_button.clicked.connect(self.scholar_button_click)
		self.citations_button.clicked.connect(self.citations_button_click)
		self.reindex_button.clicked.connect(self.reindex_button_click)


	@Slot()
	def cell_double_click(self, row, column):
		subprocess.run(['xdg-open', Index.gPapers[row]['path']], check=True)

	@Slot()
	def cell_click(self, row, column):
		self.selected_paper_index = row
		self.paper_title.setText(Index.gPapers[row]['title'])

		if 'authors' in Index.gPapers[row]:
			self.paper_authors.setText(Index.gPapers[row]['authors'])

		self.paper_tags.setText(str(Index.gPapers[row]['tags']))
		self.paper_filename.setText(Index.gPapers[row]['path'])

		if 'abstract' in Index.gPapers[row]:
			self.paper_abstract.setText(Index.gPapers[row]['abstract'])
		print('set selected_paper_index',row)

	@Slot()
	def url_button_click(self):
		webbrowser.open(Index.gPapers[self.selected_paper_index]['url'])

	@Slot()
	def google_button_click(self):
		webbrowser.open(Index.gPapers[self.selected_paper_index]['url'])

	@Slot()
	def scholar_button_click(self):
		webbrowser.open(Index.gPapers[self.selected_paper_index]['url'])

	@Slot()
	def citations_button_click(self):
		cited_string = 'https://scholar.google.co.in/scholar?cites=' + Index.gPapers[self.selected_paper_index]['cited_by_url'] + '&as_sdt=2005&sciodt=0,5&hl=en'
		webbrowser.open(cited_string)

	@Slot()
	def reindex_button_click(self):
		text, ok = QInputDialog().getText(self, "Enter search query",
                                     "Enter google scholar search query:", QLineEdit.Normal,
                                     "")
		if ok and text:
			Index.force_index_file(Index.gPapers[self.selected_paper_index]['path'], self.selected_paper_index, text)
			print(Index.gPapers[self.selected_paper_index]['authors'])
			self.cell_click(self.selected_paper_index,0)
			Index.save_json()