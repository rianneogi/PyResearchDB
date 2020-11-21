from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import (QWidget,QTabWidget,QVBoxLayout,QApplication,QLabel,QHBoxLayout)
import popplerqt5
import sys

class TestPoppler(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		self.pdf_image = QLabel('')
		self.pixmap = QPixmap()
		# self.pdf_image.setPixmap(self.pixmap)
		# self.pdf_image.show()
		self.bytearray = QByteArray()
		# self.qimage = QImage()
		self.image = QImage()

		self.pdf = popplerqt5.Poppler.Document.load('1.pdf')
		# popplerqt5.Poppler.Page()
		self.page = self.pdf.page(0)
		# self.renderer = popplerqt5.Poppler.PageRenderer()
		self.image = self.page.renderToImage(125, 125, -1, -1, 1000, 1415)
		bits = self.image.bits()
		self.image.invertPixels()
		for x in range(self.image.width()):
			for y in range(self.image.height()):
				rgb = self.image.pixelColor(x, y)
				# print(rgb.red(), rgb.blue(), rgb.green())
				if rgb.red() == 0 and rgb.blue() == 0 and rgb.green() == 0:
					rgb.setRed(68)
					rgb.setGreen(68)
					rgb.setBlue(68)
				if rgb.red() == 255 and rgb.blue() == 255 and rgb.green() == 255:
					rgb.setRed(234)
					rgb.setGreen(234)
					rgb.setBlue(234)
				self.image.setPixelColor(x,y,rgb)
		
		# self.image.
		print(bits)
		print(type(bits))
		# print(self.image.data)
		# print(image.memoryview().tolist())

		# print(type(self.image.data))
		# self.bytearray.fromRawData(self.image.data)
		# self.qimage = QImage()
		# self.qimage.loadFromData(self.bytearray)
		# self.pixmap.loadFromData(self.bytearray)
		self.pixmap = QPixmap.fromImage(self.image)
		# self.pixmap = QPixmap('pic.png')
		self.pdf_image.setPixmap(self.pixmap)
		# self.pdf_image.setScaledContents(True)
		self.pdf_image.setFixedSize(1000, 1415)
		self.pdf_image.show()
		
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.pdf_image)
		self.setLayout(self.layout)

		textlist = self.page.textList()
		# print(textlist)
		for text in textlist:
			bb = text.boundingBox()
			print('Text:',text.text(),'x:',str(bb.x()),', y:',str(bb.y()),', width:',str(bb.width()),', height:',str(bb.height()))



if __name__ == "__main__":
	# Index.load_json(Index.gJSONfilename)
	# print(Index.gPapers)
	# notify2.init("PdfDB")
	# Index.load_tags()

	app = QApplication([])

	widget = TestPoppler()
	widget.resize(1600, 1000)
	widget.show()

	sys.exit(app.exec_())