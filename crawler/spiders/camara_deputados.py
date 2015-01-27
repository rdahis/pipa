# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items

# html
import urllib

# XML Parser
from lxml.etree import fromstring


class CamaraDeputadosSpider(scrapy.Spider):
	name = "camara_deputados"
	allowed_domains = ["www.camara.gov.br"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados',
	)

	def parse(self, response):
		basic_list = fromstring(response.body)
		for deputado in basic_list.getchildren():
			id_cadastro = deputado.find('ideCadastro').text
			params = urllib.urlencode({'ideCadastro': id_cadastro, 'numLegislatura': ''})
			url = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado'
			yield scrapy.http.Request(url + '?' + params, callback=self.parse2, meta={'deputado': deputado})

	def parse2(self,r):
		deputado = r.meta['deputado']
		deputado_detalhes = fromstring(r.body).find('./Deputado')
		dep = _create_item_from_element(deputado, deputado_detalhes)
		yield dep

def _create_item_from_element(element, element_detalhes):
	out = items.DeputadoCamara()
	out['ideCadastro'] = element.find('ideCadastro').text
	out['idParlamentar'] = element.find('idParlamentar').text
	out['codOrcamento'] = element.find('codOrcamento').text
	out['condicao'] = element.find('condicao').text
	out['matricula'] = element.find('matricula').text
	#out['uf'] = element.find('uf').text
	out['fone'] = element.find('fone').text
	out['urlFoto'] = element.find('urlFoto').text
	out['numLegislatura'] = element_detalhes.find('numLegislatura').text
	out['email'] = element_detalhes.find('email').text
	out['nomeProfissao'] = element_detalhes.find('nomeProfissao').text
	out['dataNascimento'] = element_detalhes.find('dataNascimento').text
	out['dataFalecimento'] = element_detalhes.find('dataFalecimento').text
	out['ufRepresentacaoAtual'] = element_detalhes.find('ufRepresentacaoAtual').text
	out['situacaoNaLegislaturaAtual'] = element_detalhes.find('situacaoNaLegislaturaAtual').text
	out['idParlamentarDeprecated'] = element_detalhes.find('idParlamentarDeprecated').text
	out['nomeParlamentarAtual'] = element_detalhes.find('nomeParlamentarAtual').text
	out['nomeCivil'] = element_detalhes.find('nomeCivil').text
	out['sexo'] = element_detalhes.find('sexo').text
	out['idPartido'] = element_detalhes.find('./partidoAtual/idPartido').text
	out['sigla'] = element_detalhes.find('./partidoAtual/sigla').text
	out['nome'] = element_detalhes.find('./partidoAtual/nome').text
	out['numero'] = element_detalhes.find('gabinete/numero').text
	out['anexo'] = element_detalhes.find('gabinete/anexo').text
	return out

