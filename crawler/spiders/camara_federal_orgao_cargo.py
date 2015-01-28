# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items
from scrapy.http import HtmlResponse

# XML Parser
from lxml.etree import fromstring

class CamaraOrgaosCargosSpider(scrapy.Spider):
	name = "camara_orgaos_cargos"
	allowed_domains = ["www2.camara.leg.br/"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ListarCargosOrgaosLegislativosCD',
	)

	def parse(self, response):
		tree = fromstring(response.body)
		for cargo in tree.getchildren():
			i = _create_item_from_element(cargo)
			yield i

def _create_item_from_element(element):
	out = items.OrgaoCargoCamara()
	out['id'] = element.attrib['id']
	out['descricao'] = element.attrib['descricao']
	return out
