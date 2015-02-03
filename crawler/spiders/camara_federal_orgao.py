# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class CamaraOrgaosSpider(scrapy.Spider):
	name = "camara_federal_orgao"
	allowed_domains = ["www2.camara.leg.br/"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ListarTiposOrgaos',
	)

	def parse(self, response):
		tree = ET.fromstring(response.body)
		for orgao in tree.findall('./tipoOrgao'):
			i = _create_item_from_element(orgao)
			yield i

def _create_item_from_element(element):
	out = items.OrgaoCamara()
	out['id'] = element.attrib['id']
	out['descricao'] = element.attrib['descricao']
	return out
