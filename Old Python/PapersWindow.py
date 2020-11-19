# import PyPDF2 as pdf
# import textract
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
# from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PySide2.QtCore import Qt,QModelIndex,QByteArray
from PySide2.QtGui import (QImage,QPixmap)
from PySide2.QtWidgets import (QLineEdit,QInputDialog,QPushButton,QLabel,QWidget,QTableWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QAction)
# from PySide2.QtCharts import *
# from PySide2 import *
from PySide2.QtCore import Signal,Slot

import Index
import poppler
from TagsCheckbox import TagsCheckboxWindow

def getTagsString(tags):
	s = ""
	c = 0
	for tag in tags:
		s += tag
		
		if c != len(tags) - 1:
			s += ", "
		c += 1

	return s

def getAuthorName(a):
	s = ""
	if 'name' in a:
			s+= a['name']
	elif 'given' in a:
		s += a['given'] + " " + a['family']
	else:
		s += a['family']

	#post process the name so that names have a common format
	i = s.find('.')
	if i != -1 and i!=len(s)-1:
		if s[i + 1] != ' ':
			s = s[:i+1] + ' ' + s[i+1:]

	return s

def getAuthorString(authors):
	s = ""
	c = 0
	for a in authors:
		s += getAuthorName(a)

		if c != len(authors) - 1:
			s+=", "

		c+=1
	return s

def sortByTitle(json):
	return json['title']

def sortByAuthor(json):
	if 'authors' in json:
		return getAuthorString(json['authors'])
	return ''

def sortByYear(json):
	if 'year' in json:
		return json['year']
	if 'date' in json:
		return json['date'][0]
	return 0

class PapersTab(QWidget):
	def __init__(self):
		right_width = 400

		QWidget.__init__(self)
        # self.items = 0

		self.selected_paper_index = -1

		self.table = QTableWidget()
		self.table.setColumnCount(6)
		self.table.setHorizontalHeaderLabels(['Title', 'Authors', 'Tags', 'Year', 'Name', 'Abstract'])
		self.table.horizontalHeader().setSectionsMovable(True)
		self.table.setColumnWidth(0, 300)
		self.table.setColumnWidth(1, 200)
		self.table.setColumnWidth(2, 200)
		self.table.setColumnWidth(3, 100)
		self.table.setColumnWidth(4, 400)

		self.table.setRowCount(len(Index.gPapers))
		self.table.setSortingEnabled(False)
		
		# self.document = popplerqt5.Poppler.Document.load(Index.gPapers[0]['path'])
		# self.page = self.document.page(0)
		# self.image = self.page.renderToImage(0, 0, 0, 0)
		# self.preview = QLabel('')
		# self.preview.setPixmap(QPixmap.fromImage(self.image))

		# print(Index.gPapers)

		self.PapersView = Index.gPapers.copy()
		# self.PapersView.sort(key=sortByTitle)

		self.update()

		self.sort_by_title = QPushButton('Sort by Title')
		self.sort_by_author = QPushButton('Sort by Authors')
		self.sort_by_year = QPushButton('Sort by Year')
		
		self.sorting = QHBoxLayout()
		self.sorting.addWidget(self.sort_by_title)
		self.sorting.addWidget(self.sort_by_author)
		self.sorting.addWidget(self.sort_by_year)

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

		self.pdf_image = QLabel()
		self.pixmap = QPixmap()
		self.pdf_image.setPixmap(self.pixmap)
		self.pdf_image.show()
		self.bytearray = QByteArray()
		self.qimage = QImage()

		self.right = QVBoxLayout()
		self.right.addLayout(self.sorting)
		self.right.addWidget(self.paper_title)
		self.right.addWidget(self.paper_authors)
		self.right.addWidget(self.paper_tags)
		self.right.addWidget(self.pdf_image)
		self.right.addWidget(self.paper_filename)
		self.right.addWidget(self.paper_abstract)

		self.url_button = QPushButton('Link')
		self.google_button = QPushButton('Google')
		self.scholar_button = QPushButton('Scholar')
		self.citations_button = QPushButton('Citations')
		self.reindex_button = QPushButton('Reindex by Corpus ID')
		self.add_paper_button = QPushButton('Add Publication by ID')
		self.set_tags_button = QPushButton('Set Tags')

		self.buttons = QHBoxLayout()
		self.buttons.addWidget(self.set_tags_button)
		self.buttons.addWidget(self.url_button)
		# self.buttons.addWidget(self.scholar_button)
		# self.buttons.addWidget(self.google_button)
		# self.buttons.addWidget(self.citations_button)
		self.buttons.addWidget(self.reindex_button)
		self.buttons.addWidget(self.add_paper_button)

		self.right.addLayout(self.buttons)
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.table)
		self.layout.addLayout(self.right)

		self.setLayout(self.layout)

		# doubleclick_action = QAction("cellDoubleClicked", self)
		self.table.cellDoubleClicked.connect(self.cell_double_click)
		# self.table.cellClicked.connect(self.cell_click)
		self.table.selectionModel().currentRowChanged.connect(self.row_changed)

		# self.table.

		self.url_button.clicked.connect(self.url_button_click)
		self.google_button.clicked.connect(self.google_button_click)
		self.scholar_button.clicked.connect(self.scholar_button_click)
		self.citations_button.clicked.connect(self.citations_button_click)
		self.reindex_button.clicked.connect(self.reindex_button_click)
		self.add_paper_button.clicked.connect(self.add_paper_button_click)
		self.set_tags_button.clicked.connect(self.set_tags_button_click)

		self.sort_by_title.clicked.connect(self.sort_by_title_click)
		self.sort_by_author.clicked.connect(self.sort_by_author_click)
		self.sort_by_year.clicked.connect(self.sort_by_year_click)

	def update(self):
		i = 0
		for paper in self.PapersView:
			# print(paper)
			item1 = QTableWidgetItem()
			self.table.setItem(i, 0, item1)
			item1.setText(paper['title'])
			item1.setFlags(Qt.ItemIsEnabled)

			authors=''
			if 'authors' in paper:
				authors = getAuthorString(paper['authors'])
			item2 = QTableWidgetItem()
			self.table.setItem(i, 1, item2)
			item2.setText(authors)
			item2.setFlags(Qt.ItemIsEnabled)

			tags=[]
			if 'tags' in paper:
				tags = paper['tags']
			item3 = QTableWidgetItem()
			self.table.setItem(i, 2, item3)
			item3.setText(getTagsString(tags))
			item3.setFlags(Qt.ItemIsEnabled)

			date = 0
			if 'year' in paper:
				date = paper['year']
			item4 = QTableWidgetItem()
			self.table.setItem(i, 3, item4)
			if date!=0:
				item4.setText(str(date))
			else:
				item4.setText('')
			item4.setFlags(Qt.ItemIsEnabled)

			item5 = QTableWidgetItem()
			self.table.setItem(i, 4, item5)
			item5.setText(paper['path'])
			item5.setFlags(Qt.ItemIsEnabled)

			abstract=''
			if 'abstract' in paper:
				abstract = paper['abstract']
			item6 = QTableWidgetItem()
			self.table.setItem(i, 5, item6)
			item6.setText(abstract)
			item6.setFlags(Qt.ItemIsEnabled)
			
			i+=1

	@Slot()
	def cell_double_click(self, row, column):
		subprocess.run(['xdg-open', self.PapersView[row]['path']], check=True)

	# @Slot()
	# def cell_click(self, row, column):
		
		
	# 	# self.PapersView.sort(key=sortByTitle)
	# 	# self.update()

	def update_selected_paper_info(self):
		row = self.selected_paper_index
		self.paper_title.setText(self.PapersView[row]['title'])

		if 'authors' in self.PapersView[row]:
			self.paper_authors.setText(getAuthorString(self.PapersView[row]['authors']))
		else:
			self.paper_authors.setText('')

		if 'tags' in self.PapersView[row]:
			self.paper_tags.setText(getTagsString(self.PapersView[row]['tags']))
		else:
			self.paper_tags.setText('')
			
		self.paper_filename.setText(self.PapersView[row]['path'])

		if 'abstract' in self.PapersView[row]:
			self.paper_abstract.setText(self.PapersView[row]['abstract'])
		else:
			self.paper_authors.setText('')

		self.pdf = poppler.load_from_file(self.PapersView[row]['path'])
		self.page = self.pdf.create_page(0)
		self.renderer = poppler.PageRenderer()
		self.image = self.renderer.render_page(self.page)
		# print(image.data)
		# print(image.memoryview().tolist())

		print(type(self.image.data))
		self.bytearray.fromRawData(self.image.data)
		# self.qimage = QImage()
		self.qimage.loadFromData(self.bytearray)
		self.pixmap.fromImage(self.qimage)
		self.pdf_image.setPixmap(self.pixmap)
		self.pdf_image.show()

		print('set selected_paper_index', row)

	@Slot()
	def row_changed(self, curr, prev):
		self.selected_paper_index = curr.row()
		self.update_selected_paper_info()
		

	@Slot()
	def sort_by_title_click(self):
		self.PapersView.sort(key=sortByTitle)
		self.update()

	@Slot()
	def sort_by_author_click(self):
		self.PapersView.sort(key=sortByAuthor)
		self.update()

	@Slot()
	def sort_by_year_click(self):
		self.PapersView.sort(key=sortByYear)
		self.update()

	@Slot()
	def url_button_click(self):
		webbrowser.open(self.PapersView[self.selected_paper_index]['url'])

	@Slot()
	def google_button_click(self):
		webbrowser.open(self.PapersView[self.selected_paper_index]['url'])

	@Slot()
	def scholar_button_click(self):
		webbrowser.open(self.PapersView[self.selected_paper_index]['url'])

	@Slot()
	def citations_button_click(self):
		cited_string = 'https://scholar.google.co.in/scholar?cites=' + self.PapersView[self.selected_paper_index]['cited_by_url'] + '&as_sdt=2005&sciodt=0,5&hl=en'
		webbrowser.open(cited_string)

	@Slot()
	def reindex_button_click(self):
		text, ok = QInputDialog().getText(self, "Enter Corpus ID",
                                     "Enter semantic scholar Corpus ID:", QLineEdit.Normal,
                                     "")
		if ok and text:
			# Index.force_index_file(self.PapersView[self.selected_paper_index]['path'], self.selected_paper_index, text)
			Index.reindex_file_by_corpus_id(self.PapersView[self.selected_paper_index]['path'], text)
			# print(Index.gPapers[self.selected_paper_index]['authors'])
			# self.row_changed(self.selected_paper_index,0)
			self.update_selected_paper_info()
			Index.save_json(Index.gJSONfilename)
			self.PapersView = Index.gPapers.copy()
			self.update()

	@Slot()
	def add_paper_button_click(self):
		text, ok = QInputDialog().getText(self, "Enter Corpus ID",
                                     "Enter semantic scholar Corpus ID:", QLineEdit.Normal,
                                     "")
		if ok and text:
			Index.add_paper_by_corpus_id(text)
			# self.update_selected_paper_info()
			self.PapersView = Index.gPapers.copy()
			self.update()

	@Slot()
	def set_tags_button_click(self):
		print('initiating tags window')
		self.widget = TagsCheckboxWindow(self.PapersView[self.selected_paper_index]['path'])
		self.widget.resize(800, 800)
		self.widget.show()
