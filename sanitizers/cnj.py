import pdfquery
import re
import io, os
import json


path = '/Users/ricardodahis/Desktop/raw_cnj'


#dentro da classe Parse, conseguir ter dois parsers, um pra cada tipo de pdf
#cuspir pra dois jsons separados, pra ir empilhando separadamente



def main():
	# Generates empty temp json files
	output_juizes = []
	output_varas = []

	# Fills empty files with data
	for fn in os.listdir(path):
		if fn[-4:] == '.pdf':
			text_els = convert_pdf_to_txt_els(path+'/'+fn[:-3]+'pdf')
			parser = Parser()
			header, body = parser.parse(text_els)

			juiz = determines_obs_level(header)
			output = merge_two_dicts(header,body)
			if juiz:
				output_juizes.append(output)
			else:
				output_varas.append(output)

	# Saves files with full outputs
	with io.open(path+'/varas.json', 'w', encoding='utf-8') as outfile:
		outfile.write(unicode(json.dumps(output_varas,  ensure_ascii=False)))
	with io.open(path+'/juizes.json', 'w', encoding='utf-8') as outfile:
		outfile.write(unicode(json.dumps(output_juizes,  ensure_ascii=False)))
	
	

def determines_obs_level(d):
	return d.has_key('Juiz(a)')


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
		if line.isdigit():
			self.state = self._data_values
			self._data_values(line)
			return
		line = re.sub(re.compile('^[0-9]* *'), '', line)
		if ':' not in line: return
		key, _ = line.split(':')
		self.out_keys.append(key)

	def _data_values(self, line):
		if 'Corregedoria Nacional' in line:
			self.state = None
			return
		value = int(line)
		try:
			key = self.out_keys.pop(0) # FIFO
		except IndexError:
			if value == 1: return # marca o fim da pagina 1, que nao deve ser incluido
			raise
		self.out[key.strip()] = value
		
	def parse(self, text_els):
		assert type(text_els) == list, "list of elements expected"
		min_x0 = min(self._get_x0_coord_for_num_els(text_els))
		text_els_filtered = [el for el in text_els if not el.text.strip().isdigit() or float(el.attrib['x0']) > min_x0 + 10 ] # Eliminamos caras a dez pixels do mais da direita pois os numeros de 2 digitos estao em coordenadas perto, mas diferetnes
		text = [el.text for el in text_els_filtered] # for debuging help
		#assert max(['DESPACHOS PROFERIDOS EM PLANT' in string for string in text])
		import ipdb; ipdb.set_trace()
		for el in text_els_filtered:
			line = el.text.strip()
			if line and self.state:
				try: self.state(line)
				except Exception as ee:
					import ipdb; ipdb.set_trace()
					raise
		return self.header, self.out

	def _get_x0_coord_for_num_els(self, text_els):
		ret = [float(el.attrib['x0']) for el in text_els if el.text.strip().isdigit()]
		import ipdb; ipdb.set_trace()
		return ret

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def convert_pdf_to_txt_els(path):
	print('vou converter mestre!')
	pdf = pdfquery.PDFQuery(path)	
	pdf.load()
	tree = pdf.get_tree()
	root = tree.getroot()
	text_els = []
	for el in root.iterdescendants():
		if not el.text: continue
		text_els.append(el)
	return text_els

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


if __name__ == '__main__':
	main()


