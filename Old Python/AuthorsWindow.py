from PySide2.QtCore import Qt
from PySide2.QtGui import (QImage,QPixmap)
from PySide2.QtWidgets import (QHeaderView,QLineEdit,QInputDialog,QPushButton,QLabel,QWidget,QTableWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QAction)
# from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PySide2.QtCore import Signal,Slot

import subprocess

import Index
import PapersWindow


def sortByFirstName(json):
	return json['name']

def sortByLastName(json):
	return 0  # not implemented

def sortByPubs(json):
	return json['pubs']

class AuthorsTab(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		self.selected_author_index = -1
		self.selected_author_name = ""

		self.author_table = QTableWidget()
		self.author_table.setColumnCount(2)
		self.author_table.setHorizontalHeaderLabels(['Name', 'Publications'])
		self.author_table.horizontalHeader().setSectionsMovable(True)
		self.author_table.setColumnWidth(0, 200)
		self.author_table.setColumnWidth(1, 75)
		self.author_table.setSortingEnabled(False)
		# self.author_table.horizontalHeader().setMaximumWidth(225)
		self.author_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		# self.author_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		# self.author_table.setStyleSheet

		self.pubs_table = QTableWidget()
		self.pubs_table.setColumnCount(4)
		self.pubs_table.setHorizontalHeaderLabels(['Title', 'Authors', 'Tags', 'Year'])
		self.pubs_table.horizontalHeader().setSectionsMovable(True)
		self.pubs_table.setColumnWidth(0, 300)
		self.pubs_table.setColumnWidth(1, 300)
		self.pubs_table.setColumnWidth(2, 300)
		self.pubs_table.setColumnWidth(3, 100)
		self.pubs_table.setSortingEnabled(False)
		
		self.authors_dict = {}
		self.pubs_per_author = {}
		for json in Index.gPapers:
			# print(json)
			if 'authors' in json:
				for author in json['authors']:
					name = PapersWindow.getAuthorName(author)
					if name not in self.authors_dict:
						self.authors_dict[name] = {}
						self.authors_dict[name]['pubs'] = 1
						self.pubs_per_author[name] = []
						self.pubs_per_author[name].append(json)
					else:
						self.authors_dict[name]['pubs'] = self.authors_dict[name]['pubs'] + 1
						self.pubs_per_author[name].append(json)
					
		# print(self.authors_tmp)
		self.authors = []
		for author in self.authors_dict:
			self.authors.append({'name': author, 'pubs': self.authors_dict[author]['pubs']})

		self.author_table.setRowCount(len(self.authors))
		self.update_authors()

		self.sort_by_first_name = QPushButton('Sort by Name')
		self.sort_by_last_name = QPushButton('Sort by last name')
		self.sort_by_pubs = QPushButton('Sort by Publications')
		self.sort_by_title = QPushButton('Sort by Title')
		self.sort_by_year = QPushButton('Sort by Year')
		self.sort_by_recent = QPushButton('Sort by Recent')
		self.current_author_sort = 'default'
		self.current_pub_sort = 'default'

		self.author_sorting = QHBoxLayout()
		self.author_sorting.addWidget(self.sort_by_first_name)
		# self.sorting.addWidget(self.sort_by_last_name)
		self.author_sorting.addWidget(self.sort_by_pubs)

		self.pubs_sorting = QHBoxLayout()
		self.pubs_sorting.addWidget(self.sort_by_title)
		self.pubs_sorting.addWidget(self.sort_by_year)
		self.pubs_sorting.addWidget(self.sort_by_recent)

		self.sorting = QHBoxLayout()
		self.sorting.addLayout(self.author_sorting)
		self.sorting.addLayout(self.pubs_sorting)

		self.tables = QHBoxLayout()
		self.tables.addWidget(self.author_table)
		self.tables.addWidget(self.pubs_table)
		# self.layout.addLayout(self.tables)

		self.layout = QVBoxLayout()
		self.layout.addLayout(self.sorting)
		self.layout.addLayout(self.tables)

		self.setLayout(self.layout)

		self.author_table.selectionModel().currentRowChanged.connect(self.authors_row_changed)
		self.pubs_table.cellDoubleClicked.connect(self.pubs_cell_double_click)

		self.sort_by_first_name.clicked.connect(self.sort_by_first_name_click)
		self.sort_by_last_name.clicked.connect(self.sort_by_last_name_click)
		self.sort_by_pubs.clicked.connect(self.sort_by_pubs_click)
		self.sort_by_title.clicked.connect(self.sort_by_title_click)
		self.sort_by_year.clicked.connect(self.sort_by_year_click)
		self.sort_by_recent.clicked.connect(self.sort_by_recent_click)

	def update_authors(self):
		i = 0
		for author in self.authors:
			item1 = QTableWidgetItem()
			self.author_table.setItem(i, 0, item1)
			item1.setText(author['name'])
			item1.setFlags(Qt.ItemIsEnabled)

			item2 = QTableWidgetItem()
			self.author_table.setItem(i, 1, item2)
			item2.setText(str(author['pubs']))
			item2.setFlags(Qt.ItemIsEnabled)

			i += 1

	def update_pubs(self):
		self.pubs_table.setRowCount(len(self.pubs_per_author[self.selected_author_name]))

		i = 0
		for paper in self.pubs_per_author[self.selected_author_name]:
			item1 = QTableWidgetItem()
			self.pubs_table.setItem(i, 0, item1)
			item1.setText(paper['title'])
			item1.setFlags(Qt.ItemIsEnabled)

			item2 = QTableWidgetItem()
			self.pubs_table.setItem(i, 1, item2)
			item2.setText(PapersWindow.getAuthorString(paper['authors']))
			item2.setFlags(Qt.ItemIsEnabled)

			item3 = QTableWidgetItem()
			self.pubs_table.setItem(i, 2, item3)
			if 'tags' in paper:
				item3.setText(PapersWindow.getTagsString(paper['tags']))
			else:
				item3.setText('')
			item3.setFlags(Qt.ItemIsEnabled)

			item4 = QTableWidgetItem()
			self.pubs_table.setItem(i, 3, item4)
			item4.setText(str(paper['year']))
			item4.setFlags(Qt.ItemIsEnabled)

			i+=1

	# @Slot()
	# def authors_cell_click(self, row, column):
	# 	self.selected_author_index = row
	# 	self.selected_author_name = self.authors[row]['name']
	# 	self.update_pubs()
		
	# 	print('set selected_author_index', row)
		
	@Slot()
	def authors_row_changed(self, curr, prev):
		row = curr.row()
		self.selected_author_index = row
		self.selected_author_name = self.authors[row]['name']
		self.sort()
		self.update_pubs()
		
		print('set selected_author_index', row)


	@Slot()
	def pubs_cell_double_click(self, row, column):
		# subprocess.run(['xdg-open', self.pubs_per_author[self.selected_author_name][row]['path']], check=True)
		Index.open_paper(self.pubs_per_author[self.selected_author_name][row]['path'])

	def sort(self):
		if self.current_author_sort == 'name':
			self.authors.sort(key=sortByFirstName)
		if self.current_author_sort == 'name_rev':
			self.authors.sort(key=sortByFirstName, reverse=True)
			print('reverse sor tbyname')
		if self.current_author_sort == 'pubs':
			self.authors.sort(key=sortByPubs, reverse=True)
		if self.current_author_sort == 'pubs_rev':
			self.authors.sort(key=sortByPubs)

		if self.current_pub_sort == 'title':
			self.pubs_per_author[self.selected_author_name].sort(key=PapersWindow.sortByTitle)
		if self.current_pub_sort == 'title_rev':
			self.pubs_per_author[self.selected_author_name].sort(key=PapersWindow.sortByTitle, reverse=True)
		if self.current_pub_sort == 'year':
			self.pubs_per_author[self.selected_author_name].sort(key=PapersWindow.sortByYear)
		if self.current_pub_sort == 'year_rev':
			self.pubs_per_author[self.selected_author_name].sort(key=PapersWindow.sortByYear, reverse=True)
		if self.current_pub_sort == 'recent':
			self.pubs_per_author[self.selected_author_name].sort(key=PapersWindow.sortByRecent, reverse=True)
		if self.current_pub_sort == 'recent_rev':
			self.pubs_per_author[self.selected_author_name].sort(key=PapersWindow.sortByRecent)

	@Slot()
	def sort_by_first_name_click(self):
		if self.current_author_sort == 'name':
			self.current_author_sort = 'name_rev'
		else:
			self.current_author_sort = 'name'
		self.sort()
		self.update_authors()
		self.update_pubs()

	@Slot()
	def sort_by_last_name_click(self):
		if self.current_author_sort == 'name':
			self.current_author_sort = 'name_rev'
		else:
			self.current_author_sort = 'name'
		self.sort()
		self.update_authors()
		self.update_pubs()

	@Slot()
	def sort_by_pubs_click(self):
		if self.current_author_sort == 'pubs':
			self.current_author_sort = 'pubs_rev'
		else:
			self.current_author_sort = 'pubs'
		self.sort()
		self.update_authors()
		self.update_pubs()

	@Slot()
	def sort_by_title_click(self):
		if self.current_pub_sort == 'title':
			self.current_pub_sort = 'title_rev'
		else:
			self.current_pub_sort = 'title'
		self.sort()
		self.update_authors()
		self.update_pubs()
	
	@Slot()
	def sort_by_year_click(self):
		if self.current_pub_sort == 'year':
			self.current_pub_sort = 'year_rev'
		else:
			self.current_pub_sort = 'year'
		self.sort()
		self.update_authors()
		self.update_pubs()

	@Slot()
	def sort_by_recent_click(self):
		if self.current_pub_sort == 'recent':
			self.current_pub_sort = 'recent_rev'
		else:
			self.current_pub_sort = 'recent'
		self.sort()
		self.update_authors()
		self.update_pubs()