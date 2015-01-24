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
    out['id_proposicao'] = element.find('id').text
    out['nome_proposicao'] = element.find('nome').text
    out['id_tipo_proposicao'] = element.find('tipoProposicao/id').text
    out['sigla_tipo_proposicao'] = element.find('tipoProposicao/sigla').text
    out['nome_tipo_proposicao'] = element.find('tipoProposicao/nome').text
    out['numero_proposicao'] = element.find('numero').text
    out['ano'] = element.find('ano').text
    out['id_orgao_numerador'] = element.find('orgaoNumerador/id').text
    out['sigla_orgao_numerador'] = element.find('orgaoNumerador/sigla').text
    out['nome_orgao_numerador'] = element.find('orgaoNumerador/nome').text
    out['data_apresentacao'] = element.find('datApresentacao').text
    out['texto_ementa'] = element.find('txtEmenta').text
    out['texto_ementa_explicacao'] = element.find('txtExplicacaoEmenta').text
    out['id_regime'] = element.find('regime/codRegime').text
    out['texto_regime'] = element.find('regime/txtRegime').text
    out['id_apreciacao'] = element.find('apreciacao/id').text
    out['texto_apreciacao'] = element.find('apreciacao/txtApreciacao').text
    out['nome_autor'] = element.find('autor1/txtNomeAutor').text
    out['id_cadastro'] = element.find('autor1/idecadastro').text
    out['id_partido'] = element.find('autor1/codPartido').text
    out['partido_sigla'] = element.find('autor1/txtSiglaPartido').text
    out['uf'] = element.find('autor1/txtSiglaUF').text
    out['qtde_autores'] = element.find('qtdAutores').text
    out['data_despacho'] = element.find('ultimoDespacho/datDespacho').text
    out['texto_despacho'] = element.find('ultimoDespacho/txtDespacho').text
    out['id_situacao'] = element.find('situacao/id').text
    out['descricao_situacao'] = element.find('situacao/descricao').text
    out['id_orgao'] = element.find('situacao/orgao/codOrgaoEstado').text
    out['sigla_orgao'] = element.find('situacao/orgao/siglaOrgaoEstado').text
    out['id_proposicao_principal'] = element.find('situacao/principal/codProposicaoPrincipal').text
    out['proposicao_principal'] = element.find('situacao/principal/proposicaoPrincipal').text
    out['ind_genero'] = element.find('indGenero').text
    out['qtde_orgaos'] = element.find('qtdOrgaosComEstado').text
    return out
