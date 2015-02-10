# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items
from scrapy.http import HtmlResponse
import urllib

from bs4 import BeautifulSoup

class BCTaxasJuros(scrapy.Spider):
	name = "bc_taxas_juros"
	allowed_domains = ["www.bcb.gov.br"]
	start_urls = (
		'http://www.bcb.gov.br/pt-br/sfn/infopban/txcred/txjuros/Paginas/Historico.aspx',
	)

	def parse(self, response):
		param_table = response.xpath("//label/span[contains(.,'Segmento :')]/ancestor::table[1]")
		assert len(param_table) == 1
		param_table = param_table[0]
		params = _get_param_els(param_table)
		params_names = params.xpath('@name').extract()
		segmento_name, modalidade_name, encargo_name, periodo_inicial_name = params
		segmento, modalidade, encargo, periodo_inicial = params
		for seg in segmento.xpath('option'):
			text = seg.xpath('text()').extract()[0]
			if '<Selecione' in text: continue # pular o caso default do select
			value = seg.xpath('@value').extract()[0]
			payload = {segmento_name: value, modalidade_name:'0', encargo_name:'0', periodo_inicial_name:'0'}
			yield Request(self.start_urls[0], method="POST", body=urllib.urlencode(payload))



	def __lixo():
			for m in modalidade:
				pass


def _get_param_els(param_table):
	params = param_table.xpath('.//select')
	assert len(params) == 4
	return params[0], params[1], params[2], params[3]
