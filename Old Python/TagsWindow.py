from PySide2.QtCore import Qt,QModelIndex
from PySide2.QtGui import (QIcon,QImage,QPixmap)
from PySide2.QtWidgets import (QLineEdit,QInputDialog,QPushButton,QLabel,QWidget,QTableWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QAction)
# from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PySide2.QtCore import Signal,Slot
# from PySide2.QtCharts import *
# from PySide2 import *
import json
import Index
import PapersWindow
import subprocess


def sortByTags(json):
	return json['name']


def sortByPubs(json):
	return len(json['papers'])

class TagsTab(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		self.tags_dict = {}
		for tag in Index.gTags:
			self.tags_dict[tag] = {}
			self.tags_dict[tag]['papers'] = []

		for paper in Index.gPapers:
			if 'tags' in paper:
				for tag in paper['tags']:
					self.tags_dict[tag]['papers'].append(paper)

		self.tags_metadata = []
		for tag in self.tags_dict:
			self.tags_metadata.append({'name':tag, 'papers':self.tags_dict[tag]['papers']})

		self.selected_tag_index = -1
		self.tags_table = QTableWidget()
		self.tags_table.setColumnCount(2)
		self.tags_table.setHorizontalHeaderLabels(['Tag', 'Count'])
		self.tags_table.horizontalHeader().setSectionsMovable(True)
		self.tags_table.setColumnWidth(0, 200)
		self.tags_table.setColumnWidth(1, 100)
		
		self.pubs_table = QTableWidget()
		self.pubs_table.setColumnCount(4)
		self.pubs_table.setHorizontalHeaderLabels(['Title', 'Authors', 'Tags', 'Year'])
		self.pubs_table.horizontalHeader().setSectionsMovable(True)
		self.pubs_table.setColumnWidth(0, 300)
		self.pubs_table.setColumnWidth(1, 300)
		self.pubs_table.setColumnWidth(2, 300)
		self.pubs_table.setColumnWidth(3, 100)
		self.pubs_table.setSortingEnabled(False)

		self.sort_by_tag_name = QPushButton('Sort by Tag')
		self.sort_by_num_pubs = QPushButton('Sort by Count')
		self.sort_by_title = QPushButton('Sort by Title')
		self.sort_by_author = QPushButton('Sort by Authors')
		self.sort_by_year = QPushButton('Sort by Year')
		self.sort_by_recent = QPushButton('Sort by Recent')
		self.current_tag_sort = 'default'
		self.current_pub_sort = 'default'

		self.add_tag_button = QPushButton('Add Tag')
		self.add_tag_button.clicked.connect(self.add_tag_click)
		self.add_tag_button.setIcon(QIcon("Icons/add.svg"))

		self.tag_sorting = QHBoxLayout()
		self.tag_sorting.addWidget(self.sort_by_tag_name)
		self.tag_sorting.addWidget(self.sort_by_num_pubs)

		self.pubs_sorting = QHBoxLayout()
		self.pubs_sorting.addWidget(self.sort_by_title)
		self.pubs_sorting.addWidget(self.sort_by_year)
		self.pubs_sorting.addWidget(self.sort_by_recent)

		self.tags = QVBoxLayout()
		self.tags.addLayout(self.tag_sorting)
		self.tags.addWidget(self.tags_table)
		self.tags.addWidget(self.add_tag_button)

		self.pubs = QVBoxLayout()
		self.pubs.addLayout(self.pubs_sorting)
		self.pubs.addWidget(self.pubs_table)

		self.layout = QHBoxLayout()
		self.layout.addLayout(self.tags)
		self.layout.addLayout(self.pubs)

		self.setLayout(self.layout)

		self.tags_table.selectionModel().currentRowChanged.connect(self.tags_row_changed)
		self.pubs_table.cellDoubleClicked.connect(self.pubs_cell_double_click)

		self.sort_by_tag_name.clicked.connect(self.sort_by_tag_click)
		self.sort_by_num_pubs.clicked.connect(self.sort_by_pubs_click)
		self.sort_by_title.clicked.connect(self.sort_by_title_click)
		self.sort_by_year.clicked.connect(self.sort_by_year_click)
		self.sort_by_recent.clicked.connect(self.sort_by_recent_click)

		self.update_tags()

	def save_tags(self):
		with open('tags.json', 'w', encoding='utf-8') as f:
			json.dump(Index.gTags, f, ensure_ascii=False, indent=4)
			print('Tags saved')

	def update_tags(self):
		i = 0
		self.tags_table.setRowCount(len(self.tags_metadata))
		for tag in self.tags_metadata:
			item1 = QTableWidgetItem()
			self.tags_table.setItem(i, 0, item1)
			item1.setText(tag['name'])
			item1.setFlags(Qt.ItemIsEnabled)

			item2 = QTableWidgetItem()
			self.tags_table.setItem(i, 1, item2)
			item2.setText(str(len(tag['papers'])))
			item2.setFlags(Qt.ItemIsEnabled)

			i += 1

	def update_pubs(self):
		self.pubs_table.setRowCount(len(self.tags_metadata[self.selected_tag_index]['papers']))

		i = 0
		for paper in self.tags_metadata[self.selected_tag_index]['papers']:
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
	
	@Slot()
	def pubs_cell_double_click(self, row, column):
		# subprocess.run(['xdg-open', self.tags_metadata[self.selected_tag_index]['papers'][row]['path']], check=True)
		Index.open_paper(self.tags_metadata[self.selected_tag_index]['papers'][row]['path'])

	@Slot()
	def tags_row_changed(self, curr, prev):
		row = curr.row()
		self.selected_tag_index = row
		self.selected_tag_name = self.tags_metadata[row]['name']
		self.sort()
		self.update_pubs()
		
		print('set selected_tag_index', row)

	@Slot()
	def add_tag_click(self):
		text, ok = QInputDialog().getText(self, "Enter Tag",
                                     "Enter tag name:", QLineEdit.Normal,
                                     "")
		if ok and text:
			Index.gTags.append(text)
			json = {'name': text, 'papers':[]}
			self.tags_metadata.append(json)
			self.update_tags()
			self.save_tags()

	def sort(self):
		if self.current_tag_sort == 'tag':
			self.tags_metadata.sort(key=sortByTags)
		if self.current_tag_sort == 'tag_rev':
			self.tags_metadata.sort(key=sortByTags, reverse=True)
		if self.current_tag_sort == 'pubs':
			self.tags_metadata.sort(key=sortByPubs, reverse=True)
		if self.current_tag_sort == 'pubs_rev':
			self.tags_metadata.sort(key=sortByPubs)

		if self.current_pub_sort == 'title':
			self.tags_metadata[self.selected_tag_index]['papers'].sort(key=PapersWindow.sortByTitle)
		if self.current_pub_sort == 'title_rev':
			self.tags_metadata[self.selected_tag_index]['papers'].sort(key=PapersWindow.sortByTitle, reverse=True)
		if self.current_pub_sort == 'year':
			self.tags_metadata[self.selected_tag_index]['papers'].sort(key=PapersWindow.sortByYear)
		if self.current_pub_sort == 'year_rev':
			self.tags_metadata[self.selected_tag_index]['papers'].sort(key=PapersWindow.sortByYear, reverse=True)
		if self.current_pub_sort == 'recent':
			self.tags_metadata[self.selected_tag_index]['papers'].sort(key=PapersWindow.sortByRecent, reverse=True)
		if self.current_pub_sort == 'recent_rev':
			self.tags_metadata[self.selected_tag_index]['papers'].sort(key=PapersWindow.sortByRecent)

	@Slot()
	def sort_by_tag_click(self):
		if self.current_tag_sort == 'tag':
			self.current_tag_sort = 'tag_rev'
		else:
			self.current_tag_sort = 'tag'
		self.sort()
		self.update_tags()
		self.update_pubs()

	@Slot()
	def sort_by_pubs_click(self):
		if self.current_tag_sort == 'pubs':
			self.current_tag_sort = 'pubs_rev'
		else:
			self.current_tag_sort = 'pubs'
		self.sort()
		self.update_tags()
		self.update_pubs()

	@Slot()
	def sort_by_title_click(self):
		if self.current_pub_sort == 'title':
			self.current_pub_sort = 'title_rev'
		else:
			self.current_pub_sort = 'title'
		self.sort()
		self.update_tags()
		self.update_pubs()
	
	@Slot()
	def sort_by_year_click(self):
		if self.current_pub_sort == 'year':
			self.current_pub_sort = 'year_rev'
		else:
			self.current_pub_sort = 'year'
		self.sort()
		self.update_tags()
		self.update_pubs()

	@Slot()
	def sort_by_recent_click(self):
		if self.current_pub_sort == 'recent':
			self.current_pub_sort = 'recent_rev'
		else:
			self.current_pub_sort = 'recent'
		self.sort()
		self.update_tags()
		self.update_pubs()

	