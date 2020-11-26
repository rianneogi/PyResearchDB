import poppler
import json

def linear_interpolation(a, b, scale):
	assert(scale>=0 and scale<=1)
	return a + (b - a) * scale
	

def run_api():
	# pdf = Poppler.Document()
	# page = Poppler.Page()
	pdf = 0
	renderer = poppler.PageRenderer()
	renderer.set_render_hint(poppler.RenderHint.text_antialiasing)
	page = 0
	image = 0
	# byte_data = QByteArray()

	color_theme = 'light'  #allowed color themes: 'light','dark','sepia'
	
	while True:
		s = input()
		tokens = s.split(' ')

		if tokens[0] == 'open':  #open a pdf file
			pdf = poppler.load_from_file(tokens[1])
			# pdf.setRenderHint(Poppler.Document.TextAntialiasing)

		if tokens[0] == 'page':  #open a page of the current pdf
			page = pdf.create_page(int(tokens[1]))

		if tokens[0] == 'pages':  #returns number of pages
			print(str(pdf.pages))

		if tokens[0] == 'color': #set color theme
			color_theme = tokens[1]

		if tokens[0] == 'textlist':  #outputs textlist as a json file
			textlist = page.text_list()

			textlist_json = []
			for text in textlist:
				bb = text.bbox
				print(dir(bb))
				d = {'text': text.text, 'x': bb.x, 'y': bb.y, 'width': bb.width, 'height': bb.height, 'chars': []}
				for i in range(len(text.text)):
					char_bb = text.char_bbox(i)
					d['chars'].append({'char:': text.text[i], 'x': char_bb.x, 'y': char_bb.y, 'width': char_bb.width, 'height': char_bb.height})
				textlist_json.append(d)

			with open('textlist_example.json', 'w') as outfile:
				json.dump(textlist_json, outfile)

			print(json.dumps(textlist_json))

		if tokens[0] == 'render': #output pixel data to stdout
			# image = page.renderToImage(3 * 72, 3 * 72, -1, -1, -1, -1)
			image = renderer.render_page(page, 3 * 72, 3 * 72, -1, -1, -1, -1)
			print(type(image.data))
			print(image.data)

			# if color_theme == 'dark':
			# 	for x in range(image.width()):
			# 		for y in range(image.height()):
			# 			rgb = image.pixelColor(x, y)
			# 			rgb.setRed(int(linear_interpolation(234, 68, rgb.red() / 255)))
			# 			rgb.setGreen(int(linear_interpolation(234, 68, rgb.green() / 255)))
			# 			rgb.setBlue(int(linear_interpolation(234, 68, rgb.blue() / 255)))
			# 			image.setPixelColor(x, y, rgb)
						
			

		if tokens[0] == 'toc':
			toc = pdf.create_toc()

if __name__ == '__main__':
	run_api()