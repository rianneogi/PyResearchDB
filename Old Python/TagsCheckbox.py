# from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PySide2.QtCore import Qt,QModelIndex,QByteArray
from PySide2.QtGui import (QImage,QPixmap)
from PySide2.QtWidgets import (QScrollArea,QCheckBox,QLineEdit,QInputDialog,QPushButton,QLabel,QWidget,QTableWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QAction)
# from PySide2.QtCharts import *
# from PySide2 import *
from PySide2.QtCore import Signal, Slot

import Index

class TagsCheckboxWindow(QWidget):
	def __init__(self, path, owner):
		QWidget.__init__(self)
		self.path = path
		self.scroll_area = QScrollArea()
		self.num_columns = 3
		self.owner = owner
		# self.checkboxes_widget = QWidget()

		for paper in Index.gPapers:
			if paper['path'] == self.path:
				self.paper = paper

		self.columns = []
		for i in range(self.num_columns):
			layout = QVBoxLayout()
			layout.setSpacing(0)
			layout.setMargin(0)
			self.columns.append(layout)

		self.checkboxes = []
		self.tags_copy = Index.gTags.copy()
		self.tags_copy.sort(key=lambda s: s)

		count = 0
		for tag in self.tags_copy:
			checkbox = QCheckBox(tag)
			self.checkboxes.append(checkbox)
			self.columns[int((self.num_columns*count)/len(self.tags_copy))].addWidget(checkbox) #add the checkbox to the appropriate column

			if 'tags' in self.paper:
				if tag in self.paper['tags']:
					checkbox.setChecked(True)

			checkbox.clicked.connect(self.checkbox_click_creator(checkbox))
			count += 1

		# self.checkboxes_widget.setLayout(self.layout)
		# self.scroll_area.setWidget(self.checkboxes_widget)

		self.layout = QHBoxLayout()
		for col in self.columns:
			self.layout.addLayout(col)

		self.scroll_area.setLayout(self.layout)
		self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll_area.setWidgetResizable(True)

		self.full_layout = QHBoxLayout()
		self.full_layout.addWidget(self.scroll_area)

		self.setLayout(self.full_layout)

	def checkbox_click_creator(self, box):
		@Slot()
		def checkbox_click():
			if box.isChecked() == True:
				# print('checkbox for', self.path, 'is true')
				if 'tags' not in self.paper:
					self.paper['tags'] = []
				if box.text() not in self.paper['tags']:
					self.paper['tags'].append(box.text())
					Index.save_json(Index.gJSONfilename)
					# self.owner.PapersView = Index.gPapers.copy()
					# self.owner.update()
					self.owner.copy_sort_update()
				# for paper in Index.gPapers:
				# 	if paper['path'] == self.path:
				# 		if 'tags' not in paper:
				# 			paper['tags'] = []
						
				# 		if box.text() not in paper['tags']:
				# 			paper['tags'].append(box.text())
				# 			Index.save_json(Index.gJSONfilename)

				# 		break

			else:
				print('checkbox', box.text(), 'for', self.path, 'is false')
				if 'tags' not in self.paper:
					self.paper['tags'] = []
				if box.text() in self.paper['tags']:
					self.paper['tags'].remove(box.text())
					Index.save_json(Index.gJSONfilename)
					# self.owner.PapersView = Index.gPapers.copy()
					# self.owner.update()
					self.owner.copy_sort_update()
				# for paper in Index.gPapers:
				# 	if paper['path'] == self.path:
				# 		if 'tags' not in paper:
				# 			paper['tags'] = []
						
				# 		if box.text() in paper['tags']:
				# 			paper['tags'].remove(box.text())
				# 			Index.save_json(Index.gJSONfilename)
							
				# 		break

		return checkbox_click
		