# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class CamaraFederalLiderBancadaSpider(scrapy.Spider):
	name = "camara_federal_bancada_lider"
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
	out['ideCadastro'] = posicao.find('ideCadastro').text
	out['partido'] = posicao.find('partido').text
	out['uf'] = posicao.find('uf').text
	if posicao.tag == 'lider':
		out['posicao'] = 'Lider'
	elif posicao.tag == 'vice_lider':
		out['posicao'] = 'Vice-Lider'
	out['bancada_sigla'] = bancada.attrib['sigla']
	out['bancada_nome'] = bancada.attrib['nome']
	return out
