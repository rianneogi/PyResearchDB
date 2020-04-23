import os
import pdftitle
import PyPDF2
import scholarly
import notify2
import json
from crossref.restful import Works

###TODO replace scholarly with crossref api

gPapers = []
gAuthors = []
gTags = []
gWorks = Works()

def load_json():
	with open('papers.json') as f:
		global gPapers
		gPapers = json.load(f)
		# print(gPapers)

def save_json():
	with open('papers.json', 'w', encoding='utf-8') as f:
		json.dump(gPapers, f, ensure_ascii=False, indent=4)

def get_info(path):
	with open(path, 'rb') as f:
		reader = PyPDF2.PdfFileReader(f)
		info = reader.getDocumentInfo()
		# pages = reader.getNumPages()
		f.close()
		print(info)
		return info

def force_index_file(path, index, title):
	print('force index', index)

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
			search_query_scholar = scholarly.search_pubs_query(title)
			search_result_scholar = next(search_query_scholar)
			# print(search_result)

			search_query_crossref = gWorks.query(bibliographic=title).sort('relevance')
			search_result_crossref = []
			if search_query_crossref.count() != 0:
				for item in search_query_crossref:
					search_result_crossref = item
					break
			else:
				print('ERROR: search did not return any results'.title)
				raise ValueError
				
			title = search_result_crossref['title'][0]
			print(type(title))
			assert (isinstance(title, str))
			print(search_result_scholar.bib.get('title'))

			if title.lower() != search_result_scholar.bib.get('title').lower():
				print("ERROR: title doesnt match from two queries, crossref:",title,"scholar:",search_result_scholar.bib.get('title'))
				raise ValueError

			abstract = search_result_scholar.bib.get('abstract')
			authors = search_result_crossref['author']
			url = search_result_crossref['URL']
			# search_result.get_citedby()
			cited_by_url = ""
			citations = 0

			if hasattr(search_result_scholar, 'id_scholarcitedby'):
				cited_by_url = search_result_scholar.id_scholarcitedby

			if hasattr(search_result_scholar, 'citedby'):
				citations = search_result_scholar.citedby

			if index==-1:
				gPapers.append({
					'path': path,
					'title': title,
					'authors': authors,
					'tags': [],
					'abstract': abstract,
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
					'abstract': abstract,
					'url': url,
					'citations': citations,
					'cited_by_url': cited_by_url
				}

			n = notify2.Notification("Document Parsed Fully", title+'\n'+authors, "package-install")
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
			
def index_file(path):
	found = False
	for i in gPapers:
		if i['path'] == path:
			found = True
			break

	if not found:
		force_index_file(path,-1,"")
		
			
def reparse_files():
	for i in range(len(gPapers)):
		if 'authors' not in gPapers[i]:
			force_index_file(gPapers[i]['path'],i,"")
			save_json()

def index_dir(path):
	for f in os.listdir(path):
		if f.endswith('.pdf'):
			index_file(path + f)
			save_json()

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

