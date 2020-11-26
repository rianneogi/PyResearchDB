from PyQt5.QtCore import QByteArray,QIODevice,QBuffer
from PyQt5.QtGui import QPixmap,QImage,QColor
from popplerqt5 import Poppler as Poppler
import sys
import json
from ctypes import c_void_p

def linear_interpolation(a, b, scale):
	assert(scale>=0 and scale<=1)
	return a + (b - a) * scale
	

def run_api():
	# pdf = Poppler.Document()
	# page = Poppler.Page()
	pdf = 0
	page = 0
	image = QImage()
	byte_data = QByteArray()

	color_theme = 'light'  #allowed color themes: 'light','dark','sepia'
	
	while True:
		s = input()
		tokens = s.split(' ')

		if tokens[0] == 'open':  #open a pdf file
			pdf = Poppler.Document.load(tokens[1])
			pdf.setRenderHint(Poppler.Document.TextAntialiasing)

		if tokens[0] == 'page':  #open a page of the current pdf
			page = pdf.page(tokens[1])

		if tokens[0] == 'pages':  #returns number of pages
			print(pdf.numPages())

		if tokens[0] == 'color': #set color theme
			color_theme = tokens[1]

		if tokens[0] == 'textlist':  #outputs textlist as a json file
			textlist = page.textList()

			textlist_json = []
			for text in textlist:
				bb = text.boundingBox()
				d = {'text': text.text(), 'x': bb.x(), 'y': bb.y(), 'width': bb.width(), 'height': bb.height()}
				textlist_json.append(d)

			print(json.dumps(textlist_json))

		if tokens[0] == 'render': #output pixel data to stdout
			image = page.renderToImage(3 * 72, 3 * 72, -1, -1, -1, -1)
			print(image.format())
			if color_theme == 'dark':
				for x in range(image.width()):
					for y in range(image.height()):
						rgb = image.pixelColor(x, y)
						rgb.setRed(int(linear_interpolation(234, 68, rgb.red() / 255)))
						rgb.setGreen(int(linear_interpolation(234, 68, rgb.green() / 255)))
						rgb.setBlue(int(linear_interpolation(234, 68, rgb.blue() / 255)))
						image.setPixelColor(x, y, rgb)
						
			# print(image.data)
			# bits = image.bits()
			# byte_data.fromRawData(image.data)
			# print(byte_data)
			ba = QByteArray()
			buffer  = QBuffer(ba)
			buffer.open(QIODevice.WriteOnly)
			image.save(buffer, "PNG")  # writes image into ba in PNG format
			ba2 = buffer.data()
			for i in ba.
			
			bits = image.constBits()
			bits.setsize(image.width() * image.height() * 4)
			print(str(bits))
			print(dir(bits))
			print(bits.asarray())
			print(str(bits.asarray()))
			imgPtr = c_void_p(bits.__int__())
			print(dir(imgPtr))
			# for i in range(len(bits)):
				# print(bits[i])
			# print(image.constBits()[0])
			# print(bits)
			# print(type(bits))
			# for i in range(image.width()):
			# 	for j in range(image.height()):
			# 		# print(image.pixel(i, j))
			# 		print(bits[i])
			# 		# color = QColor(image.pixel(i,j))
			# 		# print(image.pixel(i,j).red(), image.pixel(i,j).green(), image.pixel(i,j).blue())	

		if tokens[0] == 'toc':
			toc = pdf.toc()

if __name__ == '__main__':
	run_api()