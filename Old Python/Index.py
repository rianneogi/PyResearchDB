import os
import pdftitle
import PyPDF2
import scholarly
import notify2
import json
from crossref.restful import Works
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import bibtexparser
import semanticscholar
import time
import requests
import subprocess

gPapers = []
gTags = []
gWorks = Works()
gJSONfilename = 'papers.json'
gDefaultDownloadPath = '/home/rian/Documents/Research Papers/TCS/'

def load_tags():
	with open('tags.json', encoding='utf-8') as f:
		print('loading tags')
		global gTags
		gTags = json.load(f)

	print(gTags)

def load_json(filename):
	print('Loading json')
	with open(filename, encoding='utf-8') as f:
		global gPapers
		gPapers = json.load(f)
		# print(gPapers)
	print('Loading done')

def save_json(filename):
	print('Saving json : DONT QUIT')
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(gPapers, f, ensure_ascii=False, indent=4)
	print('Saving done')

def get_info(path):
	with open(path, 'rb') as f:
		reader = PyPDF2.PdfFileReader(f)
		info = reader.getDocumentInfo()
		# pages = reader.getNumPages()
		f.close()
		# print(info)
		return info

def query_google_scholar(title):
	search_query_scholar = scholarly.search_pubs_query(title)
	search_result_scholar = next(search_query_scholar)
	print(search_result_scholar)
	print(search_result_scholar.bib.get('author'))
	print(search_result_scholar.bib.get('doi'))
	# print(search_result_scholar.bibtex)
	driver = webdriver.Firefox()
	driver.get(search_result_scholar.url_scholarbib)
	content = driver.page_source
	soup = BeautifulSoup(content)
	bibtex = bibtexparser.loads(soup.getText())
	for entry in bibtex.entries:
		title = entry['title']
		authors = entry['author']
		print(title, authors)
		break

def query_semantic_scholar(title):
	title = title.replace(' ', '%20')
	title = title.replace(',', '%2C')
	# title = title.replace('-', '')
	title = title.replace(':', '')
	title = title.replace(';', '')
	title = title.replace('/', '%2F')

	options = FirefoxOptions()
	options.add_argument('--headless')
	driver = webdriver.Firefox(options=options)
	driver.get('https://www.semanticscholar.org/search?q=' + title + '&sort=relevance')
	content = driver.page_source
	soup = BeautifulSoup(content, features="lxml")
	for link in soup.find_all('a'):
		if link.get('data-selenium-selector')=='title-link':
			href = link.get('href')
			driver.get('https://www.semanticscholar.org' + href)

			content2 = driver.page_source
			soup2 = BeautifulSoup(content2, features="lxml")

			for span in soup2.find_all('span'):
				if span.get('data-selenium-selector') == 'corpus-id':
					text = span.text
					# print(text)
					text = text.replace(' ', '')
					print(text)
					driver.quit()
					return query_semantic_scholar_by_id(text)

			break

	print('ERROR: Semantic scholar did not return any results for', title)
	driver.quit()
	return {'title': 'Unindexed document'}
	

def query_semantic_scholar_by_id(paper_id):
	paper = semanticscholar.paper(paper_id, timeout=10)
	print(paper.keys())

	print(paper['title'])
	for author in paper['authors']:
		print(author['name'])
	return paper

def force_index_file(path, index, title): #uses crossref; deprecated
	print('force index', path, index, title)

	if title=="":
		try:
			title = pdftitle.get_title_from_file(path)
			print("Title: ", title, path)
		except:
			try:
				title = get_info(path).get('/Title')
				print("Title: ", title, path)

				if title == "" or title==None:
					print("Unable to get title of file", path)
			except:
				print("Unable to get title of file", path)

	if title!="" and title!=None:
		try:
			# search_query_scholar = scholarly.search_pubs_query(title)
			# search_result_scholar = next(search_query_scholar)
			# print(search_result_scholar)

			search_query_crossref = gWorks.query(bibliographic=title).sort('relevance')
			search_result_crossref = []
			if search_query_crossref.count() != 0:
				for item in search_query_crossref:
					search_result_crossref = item
					break
			else:
				print('ERROR: crossref search did not return any results',title)
				raise ValueError
				
			title = search_result_crossref['title'][0]
			print(title)
			print(type(title))
			assert (isinstance(title, str))
			# print(search_result_scholar.bib)
			# print(type(search_result_scholar.bib.get('title')))
			# title2 = search_result_scholar.bib.get('title')

			# if title.lower() != title2.lower():
			# 	print("ERROR: title doesnt match")
			# 	# print("ERROR: title doesnt match from two queries, crossref:",title,"scholar:",title2)
			# 	# print(title)
			# 	# print(title2)
			# 	raise ValueError

			# abstract = search_result_scholar.bib.get('abstract')
			authors = search_result_crossref['author']
			url = search_result_crossref['URL']

			date = [0,0,0]
			if 'published-online' in search_result_crossref:
				date = search_result_crossref['published-online']['date-parts'][0]
			elif 'published-print' in search_result_crossref:
				date = search_result_crossref['published-print']['date-parts'][0]
			
			# search_result.get_citedby()
			cited_by_url = ""
			citations = 0

			# if hasattr(search_result_scholar, 'id_scholarcitedby'):
			# 	cited_by_url = search_result_scholar.id_scholarcitedby

			# if hasattr(search_result_scholar, 'citedby'):
			# 	citations = search_result_scholar.citedby

			if index==-1:
				gPapers.append({
					'path': path,
					'title': title,
					'authors': authors,
					'tags': [],
					# 'abstract': abstract,
					'date': date,
					'url': url,
					'citations': citations,
					'cited_by_url': cited_by_url
				})
			else:
				gPapers[index] = {
					'path': path,
					'title': title,
					'authors': authors,
					'tags': [],
					# 'abstract': abstract,
					'date': date,
					'url': url,
					'citations': citations,
					'cited_by_url': cited_by_url
				}

			n = notify2.Notification("Document Parsed Fully", title, "package-install")
			n.show()
		except Exception as e: 
			print(e)
			if index==-1:
				gPapers.append({
					'path': path,
					'title': title,
					'tags': []
				})
			else:
				gPapers[index] = {
					'path': path,
					'title': title,
					'tags': []
				}

			n = notify2.Notification("Document Parsed Partially", title, "package-installed-outdated")
			n.show()
	else:
		if index == -1:
			gPapers.append({
				'path': path,
				'title': 'Untitled Document',
				'tags': []
			})
		else:
			gPapers[index] = {
				'path': path,
				'title': 'Untitled Document',
				'tags': []
			}

		n = notify2.Notification("Unable to get title", "Untitled Document - "+path, "package-broken")
		n.show()
			
def index_file(path, title):
	found = False
	for i in gPapers:
		# print(i['path'], path)
		if i['path'] == path:
			found = True
			break

	if not found:
		# force_index_file(path,-1,"")
		index_file_with_semantic_scholar(path, title)
		save_json(gJSONfilename)
		
			
def reparse_files():
	for i in range(len(gPapers)):
		if 'authors' not in gPapers[i]:
			force_index_file(gPapers[i]['path'],i,"")
			save_json(gJSONfilename)

def index_dir(path):
	files = os.listdir(path)
	count = 0
	file_length = len(files)
	for f in files:
		if f.endswith('.pdf'):
			index_file(path + f, f)
		count += 1
		print("Indexed " + str(count) + "/" + str(file_length))

def reindex_file_by_corpus_id(path, corpus_id):
	print('querying by corpus id:', corpus_id)
	json = query_semantic_scholar_by_id('CorpusID:'+corpus_id)
	json['path'] = path
	json['tags'] = []

	found = False
	for i in range(len(gPapers)):
		if gPapers[i]['path'] == path:
			gPapers[i] = json
			found = True

	if not found:
		gPapers.append(json)

	if json['title'] == 'Unindexed document':
		n = notify2.Notification("Unable to find publication", path, "package-broken")
		n.show()
	else:
		n = notify2.Notification("Document Parsed", json['title'], "package-install")
		n.show()


def index_file_with_semantic_scholar(path, title):
	title = title[:-4]  #remove .pdf
	print("querying:", title)
	json = query_semantic_scholar(title)
	json['path'] = path
	json['tags'] = []
	gPapers.append(json)

	if json['title'] == 'Unindexed document':
		n = notify2.Notification("Unable to find publication", title, "package-broken")
		n.show()
	else:
		n = notify2.Notification("Document Parsed", json['title'], "package-install")
		n.show()
		

# def index_with_semantic_scholar(path):
# 	with open('papers_ss.json') as f:
# 		global gPapers
# 		gPapers = json.load(f)

# 	for f in os.listdir(path):
# 		if f.endswith('.pdf'):
# 			index_file_with_semantic_scholar(path + f, f)
# 			time.sleep(5)
# 			save_json(gJSONfilename)
	
# 	with open('papers_ss.json', 'w', encoding='utf-8') as f:
# 		json.dump(gPapers, f, ensure_ascii=False, indent=4)

def add_paper_by_corpus_id(corpus_id):
	print('adding paper by corpus id', corpus_id)

	#make sure corpus id isnt already in database
	for paper in gPapers:
		# print('comparing', paper['corpusId'], corpus_id, paper['corpusId']==corpus_id)
		if int(paper['corpusId']) == int(corpus_id):
			print('This paper already exists in the database. Opening the paper instead.')
			subprocess.run(['xdg-open', paper['path']], check=True)
			return

	json = query_semantic_scholar_by_id("CorpusID:"+corpus_id)

	if json is not None:
		options = FirefoxOptions()
		options.add_argument('--headless')
		driver = webdriver.Firefox(options=options)
		driver.get(json['url'])
		content = driver.page_source
		soup = BeautifulSoup(content, features="lxml")
		pdf_found = False
		path = gDefaultDownloadPath
		for link in soup.find_all('a'):
			if link.get('data-selenium-selector')=='paper-link':
				href = link.get('href')
				print('paper link found', href)
				r = requests.get(href, allow_redirects=True)
				print('paper link type:', r.headers.get('content-type'))

				if r.headers.get('content-type').split(';')[0] == 'application/pdf':
					print('pdf found', href)
					pdf_found = True
					# driver.get(href)
					if href.find('/'):
						# print(href.rsplit('/', 1)[1]
						path += href.rsplit('/', 1)[1]
						# print('last 4 chars of path: ', path[-4:])
						if path[-4:] != '.pdf':
							path += '.pdf'
					else:
						path += 'CorpusID:' + corpus_id+'.pdf'

					if os.path.exists(path):
						path = path[:-4] + ' CorpusID:' + corpus_id+'.pdf' #remove .pdf and add corpus_id.pdf
						
						if os.path.exists(path):
							print('Unable to download: file already exists!')
							break
					
					r = requests.get(href, allow_redirects=True)
					open(path, 'wb').write(r.content)
					print('saved pdf to', path)
					break

		if pdf_found:
			json['path'] = path
			json['tags'] = []
			gPapers.append(json)
			subprocess.run(['xdg-open', json['path']], check=True) #open the paper
			n = notify2.Notification("Document Parsed", json['title'], "package-install")  #send notification
			n.show()
			save_json(gJSONfilename) #save json
		else:
			print('ERROR: Paper found but no PDF is available!')
	else:
		print("Error: corpus id not found")

def remove_dupes():
	for i in range(len(gPapers)):
		if i >= len(gPapers):
			break
		for j in range(i + 1, len(gPapers)):
			if j >= len(gPapers):
				break
			if gPapers[i]['path'] == gPapers[j]['path']:
				if 'authors' in gPapers[i]:
					print('removing ',gPapers[j]['title'])
					gPapers.remove(gPapers[j])
					j -= 1
				else:
					print('removing ',gPapers[i]['title'])
					gPapers.remove(gPapers[i])
					j -= 1
					i -= 1


def remove_unindexed_files():
	for i in range(len(gPapers)):
		if i >= len(gPapers):
			break

		if gPapers[i]['title'] == 'Unindexed document':
			gPapers.pop(i)
			i -= 1


def remove_nonexistent_files():
	for paper in gPapers:
		if not os.path.isfile(paper['path']):
			print('removing ', paper['path'], ':', paper['title'])
			gPapers.remove(paper)


def open_paper(path):
	subprocess.run(['xdg-open', path], check=True)
	for p in gPapers:
		if p['path'] == path:
			p['last-opened'] = time.time()
			print('setting last opened time to ', p['last-opened'])
		
	save_json(gJSONfilename)