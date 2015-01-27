# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items

# html
import urllib

# XML Parser
from lxml.etree import fromstring

# Datetime
from datetime import date, timedelta

# Copy
from copy import copy


class CamaraSessoesSpider(scrapy.Spider):
	name = "camara_sessoes"
	allowed_domains = ["www.camara.gov.br"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/sessoesreunioes.asmx?op=ListarPresencasDia',
	)

	def parse(self, response):
		for delta in xrange(0,100):
			url = 'http://www.camara.gov.br/SitCamaraWS/sessoesreunioes.asmx/ListarPresencasDia'
			data_raw = date.today() - timedelta(days=delta)
			data = data_raw.strftime('%d/%m/%Y')
			params = urllib.urlencode({
					'data': data,
					'numMatriculaParlamentar': '',
					'siglaPartido': '',
					'siglaUF': ''
					 })
			yield scrapy.http.Request(url + '?' + params, callback=self.parse2)

	def parse2(self, res):
		for parlamentar in fromstring(res.body).findall('./parlamentares/parlamentar'):
			pres_sessoes = _create_item_from_element(parlamentar)
			for pres_sessao in pres_sessoes:
				yield pres_sessao

def _create_item_from_element(element):
	out = items.PresencaSessaoDeputadoCamara()
	out['carteiraParlamentar'] = element.find('carteiraParlamentar').text
	out['nomeParlamentar'] = element.find('nomeParlamentar').text
	out['siglaPartido'] = element.find('siglaPartido').text
	out['siglaUF'] = element.find('siglaUF').text
	out['descricaoFrequenciaDia'] = element.find('descricaoFrequenciaDia').text
	out['justificativa'] = element.find('justificativa').text
	out['presencaExterna'] = element.find('presencaExterna').text
	ret = []
	for sessao in element.findall('./sessoesDia/sessaoDia'):
		out_sub = copy(out)
		out_sub['sessaoDia_inicio'] = sessao.find('inicio').text
		out_sub['sessaoDia_descricao'] = sessao.find('descricao').text
		out_sub['sessaoDia_frequencia'] = sessao.find('frequencia').text
		ret.append(out_sub)
	return ret
