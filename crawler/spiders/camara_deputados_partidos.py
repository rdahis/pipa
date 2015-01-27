# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class CamaraPartidosSpider(scrapy.Spider):
	name = "camara_deputados_partidos"
	allowed_domains = ["www2.camara.leg.br/"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterPartidosCD',
	)

	def parse(self, response):
		tree = ET.fromstring(response.body)
		for partido in tree.getchildren():
			p = _create_item_from_element(partido)
			yield p

def _create_item_from_element(element):
	out = items.PartidoCamara()
	out['idPartido'] = element.find('idPartido').text
	out['siglaPartido'] = element.find('siglaPartido').text
	out['nomePartido'] = element.find('nomePartido').text
	out['dataCriacao'] = element.find('dataCriacao').text
	out['dataExtincao'] = element.find('dataExtincao').text
	return out
