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
from PySide2 import QtCore, QtWidgets, QtGui
from crossref.restful import Works

from selenium import webdriver
from bs4 import BeautifulSoup

import pdfreader
import PIL

import pdflatex

# import pandas as pd

# class MyWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

#         self.button = QtWidgets.QPushButton("Click me!")
#         self.text = QtWidgets.QLabel("Hello World")
#         self.text.setAlignment(QtCore.Qt.AlignCenter)

#         self.layout = QtWidgets.QVBoxLayout()
#         self.layout.addWidget(self.text)
#         self.layout.addWidget(self.button)
#         self.setLayout(self.layout)

#         self.button.clicked.connect(self.magic)


#     def magic(self):
#         self.text.setText(random.choice(self.hello))

def get_info(path):
	with open(path, 'rb') as f:
		reader = pdf.PdfFileReader(f)
		info = reader.getDocumentInfo()
		# pages = reader.getNumPages()
		f.close()
		# print(info)
		return info

from pdfreader import SimplePDFViewer, PageDoesNotExist

fd = open('3.pdf', "rb")
viewer = SimplePDFViewer(fd)

plain_text = ""
pdf_markdown = ""
images = []
try:
    while True:
        viewer.render()
        pdf_markdown += viewer.canvas.text_content
        plain_text += "".join(viewer.canvas.strings)
        images.extend(viewer.canvas.inline_images)
        images.extend(viewer.canvas.images.values())
        viewer.next()
except PageDoesNotExist:
    pass

# pimg = PIL.Image()

print(plain_text)
print(pdf_markdown)
for img in images:
	pimg = img.to_Pillow()
	# pimg = PIL.Image()
	print(pimg.size)
	pimg.show()
	break




# driver = webdriver.Firefox()
# products=[] #List to store name of the product
# prices=[] #List to store price of the product
# ratings=[] #List to store rating of the product
# driver.get("https://scholar.google.co.in/scholar?hl=en&as_sdt=0%2C5&q=submodular+functions&btnG=")
# content = driver.page_source
# # print(content)
# soup = BeautifulSoup(content)
# # print(soup.gs_a)
# # print(soup)
# # print(soup.findAll('div'))
# for a in soup.findAll('div', attrs={'class': 'gs_a'}):
# 	print(a.text)

# for a in soup.findAll('h3', attrs={'class': 'gs_rt'}):
# 	print(a.text)

# print(products)

# works = Works()

# title = 'maximizing non-monotone submodular functions'

# # search_query = scholarly.search_pubs_query(title)
# # search_result = next(search_query)
# # print(search_result)
# # doi = search_result.doi

# # title = get_info('2.pdf').get('/Title')
# # print(title)
# # w1 = works.doi('10.1137/090779346')
# # print(w1)

# q = works.query(bibliographic=title).sort('relevance')
# if q.count != 0:
#     for item in q:
#         print(item['title'])
#         break


    # print(w1.count())
    # for item in w1:
    #     print(item['title'])

# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])

#     widget = MyWidget()
#     widget.resize(800, 600)
#     widget.show()

#     sys.exit(app.exec_())

# get_info('2.pdf')
# text = textract.process('2.pdf', method='pdftotext', layout=True)
# print(text)

# notify2.init("PdfDB")
# n = notify2.Notification("Notify", "bla", "x-office-document")
# n.show()

# filename = '4.pdf'
# get_info(filename)
# try:
#     title = pdftitle.get_title_from_file(filename)
#     print("Title: ", title)
# except:
#     title = get_info(filename).get('/Title')
#     print("Title: ", title)

#     if title == "":
#         print("Unable to get title of pdf",filename)

# search_query = scholarly.search_pubs_query(title)
# search_result = next(search_query)
# print(search_result)

# if hasattr(search_result,'id_scholarcitedby'):
#     cited_by = search_result.id_scholarcitedby
#     cited_string = 'https://scholar.google.co.in/scholar?cites=' + cited_by + '&as_sdt=2005&sciodt=0,5&hl=en'
#     webbrowser.open(cited_string)

# print(search_result.get_citedby())

