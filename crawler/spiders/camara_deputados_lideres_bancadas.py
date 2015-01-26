# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class LideresBancadasSpider(scrapy.Spider):
	name = "camara_deputados_lideres_bancadas"
	allowed_domains = ["www2.camara.leg.br/"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterLideresBancadas',
	)

	def parse(self, response):
		tree = ET.fromstring(response.body)
		for bancada in tree.getchildren():
			for posicao in bancada.getchildren():
				i = _create_item_from_element(posicao, bancada)
				yield i

def _create_item_from_element(posicao, bancada):
	out = items.LiderBancada()
	out['nome'] = posicao.find('nome').text
	out['id_cadastro'] = posicao.find('ideCadastro').text
	out['partido'] = posicao.find('partido').text
	out['uf'] = posicao.find('uf').text
	if posicao.tag == 'lider':
		out['posicao'] = 'Lider'
	elif posicao.tag == 'vice_lider':
		out['posicao'] = 'Vice-Lider'
	out['bancada'] = bancada.attrib['sigla']
	out['bancada_nome'] = bancada.attrib['nome']
	return out
