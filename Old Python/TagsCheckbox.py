# from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PySide2.QtCore import Qt,QModelIndex,QByteArray
from PySide2.QtGui import (QImage,QPixmap)
from PySide2.QtWidgets import (QCheckBox,QLineEdit,QInputDialog,QPushButton,QLabel,QWidget,QTableWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QApplication,QTableWidgetItem,QAbstractItemView,QAction)
# from PySide2.QtCharts import *
# from PySide2 import *
from PySide2.QtCore import Signal, Slot

import Index


class TagsCheckboxWindow(QWidget):
	def __init__(self, path):
		QWidget.__init__(self)
		self.path = path

		for paper in Index.gPapers:
			if paper['path'] == self.path:
				self.paper = paper

		self.layout = QVBoxLayout()
		self.checkboxes = []
		for tag in Index.gTags:
			checkbox = QCheckBox(tag)
			self.layout.addWidget(checkbox)
			self.checkboxes.append(checkbox)

			if 'tags' in self.paper:
				if tag in self.paper['tags']:
					checkbox.setChecked(True)

			checkbox.clicked.connect(self.checkbox_click_creator(checkbox))

		self.setLayout(self.layout)

	def checkbox_click_creator(self, box):
		@Slot()
		def checkbox_click():
			if box.isChecked() == True:
				print('checkbox for', self.path, 'is true')
				if 'tags' not in self.paper:
					self.paper['tags'] = []
				if box.text() not in self.paper['tags']:
					self.paper['tags'].append(box.text())
					Index.save_json(Index.gJSONfilename)
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
				# for paper in Index.gPapers:
				# 	if paper['path'] == self.path:
				# 		if 'tags' not in paper:
				# 			paper['tags'] = []
						
				# 		if box.text() in paper['tags']:
				# 			paper['tags'].remove(box.text())
				# 			Index.save_json(Index.gJSONfilename)
							
				# 		break

		return checkbox_click
		