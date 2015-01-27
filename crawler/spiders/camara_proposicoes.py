# -*- coding: utf-8 -*-
import scrapy
import crawler.items as items
from scrapy.http import HtmlResponse

# html
import urllib

# XML Parser
from lxml.etree import fromstring


class CamaraProposicoesSpider(scrapy.Spider):
	name = "camara_proposicoes"
	allowed_domains = ["www.camara.gov.br"]
	start_urls = (
		'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados',
	)

	def parse(self, response):
		basic_list = fromstring(response.body)
		for deputado in basic_list.getchildren():
			nome_parlamentar = deputado.find('nomeParlamentar').text
			nome_parlamentar_enc = nome_parlamentar.encode('utf-8')
			params = urllib.urlencode({
					'sigla': '',
					'numero': '',
					'ano': '',
					'datApresentacaoIni': '',
					'datApresentacaoFim': '',
					'idTipoAutor': '',
					'parteNomeAutor': nome_parlamentar_enc,
					'siglaPartidoAutor': '',
					'siglaUFAutor': '',
					'generoAutor': '',
					'codEstado': '',
					'codOrgaoEstado': '',
					'emTramitacao': ''
					})
			url = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes' + '?' + params
			yield scrapy.http.Request(url, callback=self.parse2)
	
	def parse2(self,r):
		for proposicao in fromstring(r.body).getchildren():
			prop = _create_item_from_element(proposicao)
			yield prop

def _create_item_from_element(element):
	out = items.ProposicaoCamara()
	out['id'] = element.find('id').text
	out['nome'] = element.find('nome').text
	out['tipoProposicao_id'] = element.find('tipoProposicao/id').text
	out['tipoProposicao_sigla'] = element.find('tipoProposicao/sigla').text
	out['tipoProposicao_nome'] = element.find('tipoProposicao/nome').text
	out['numero'] = element.find('numero').text
	out['ano'] = element.find('ano').text
	out['orgaoNumerador_id'] = element.find('orgaoNumerador/id').text
	out['orgaoNumerador_sigla'] = element.find('orgaoNumerador/sigla').text
	out['orgaoNumerador_nome'] = element.find('orgaoNumerador/nome').text
	out['dataApresentacao'] = element.find('datApresentacao').text
	out['txtEmenta'] = element.find('txtEmenta').text
	out['txtExplicacaoEmenta'] = element.find('txtExplicacaoEmenta').text
	out['codRegime'] = element.find('regime/codRegime').text
	out['txtRegime'] = element.find('regime/txtRegime').text
	out['apreciacao_id'] = element.find('apreciacao/id').text
	out['apreciacao_txtApreciacao'] = element.find('apreciacao/txtApreciacao').text
	out['txtNomeAutor'] = element.find('autor1/txtNomeAutor').text
	out['ideCadastro'] = element.find('autor1/idecadastro').text
	out['codPartido'] = element.find('autor1/codPartido').text
	out['txtSiglaPartido'] = element.find('autor1/txtSiglaPartido').text
	out['txtSiglaUF'] = element.find('autor1/txtSiglaUF').text
	out['qtdeAutores'] = element.find('qtdAutores').text
	out['datDespacho'] = element.find('ultimoDespacho/datDespacho').text
	out['txtDespacho'] = element.find('ultimoDespacho/txtDespacho').text
	out['situacao_id'] = element.find('situacao/id').text
	out['situacao_descricao'] = element.find('situacao/descricao').text
	out['codOrgaoEstado'] = element.find('situacao/orgao/codOrgaoEstado').text
	out['siglaOrgaoEstado'] = element.find('situacao/orgao/siglaOrgaoEstado').text
	out['codProposicaoPrincipal'] = element.find('situacao/principal/codProposicaoPrincipal').text
	out['proposicaoPrincipal'] = element.find('situacao/principal/proposicaoPrincipal').text
	out['indGenero'] = element.find('indGenero').text
	out['qtdOrgaosComEstado'] = element.find('qtdOrgaosComEstado').text
	return out
