import pdfquery
import re

import json

path = '/Users/ricardodahis/Desktop/raw_cnj'
path_pdf = '/Users/ricardodahis/Desktop/raw_cnj/agudo_1_2009.pdf'

def main():
	text = convert_pdf_to_txt(path+'/agudo_1_2009.pdf')
	#with open(path+'/output.txt', 'w') as text_file:
	#	text_file.write(words)
	parser = Parser()
	a,b = parser.parse(text)
	from pprint import pprint
	print(json.dumps(a, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
	print(json.dumps(b, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))




class Parser():
	def __init__(self):
		self.state = self._initial
		self.header = {}
		self.out = {}
		self.out_keys = []

	def _initial(self, line):
		if ':' in line:
			self.state = self._header
			self._header(line)
	
	def _header(self, line):
		if 'QUESTION' in line and ':' not in line:
			self.state = self._data
			return
		key, value = line.split(':')
		self.header[key.strip()] = value.strip()

	def _data(self, line):
		regexp = re.compile('^[0-9]* *')
		line = re.sub(regexp, '', line)
		if 'Total' == line:
			self.state = self._data_values
		if not line or ':' not in line: return
		key, _ = line.split(':')
		self.out_keys.append(key)

	def _data_values(self, line):
		if 'Corregedoria Nacional' in line:
			self.state = None
			return
		value = int(line)
		key = self.out_keys.pop(0) # FIFO
		self.out[key.strip()] = value
		
	def parse(self, text):
		if type(text) == str:
			text = text.split('\n')
		for line in text:
			line = line.strip()
			if line and self.state:
				try: self.state(line)
				except Exception as ee:
					import ipdb; ipdb.set_trace()
					raise
		return self.header, self.out

def convert_pdf_to_txt(path):
	pdf = pdfquery.PDFQuery(path)	
	pdf.load()
	tree = pdf.get_tree()
	root = tree.getroot()
	text = []
	for el in root.iterdescendants():
		if not el.text: continue
		text.append(el.text)
	return text

if __name__ == '__main__':
	main()
