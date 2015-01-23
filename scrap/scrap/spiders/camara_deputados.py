# -*- coding: utf-8 -*-
import scrapy
import scrap.items as items

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
    out['id_cadastro'] = element.find('ideCadastro').text
    out['id_deputado_federal'] = element.find('idParlamentar').text
    out['id_orcamento'] = element.find('codOrcamento').text
    out['condicao'] = element.find('condicao').text
    out['matricula'] = element.find('matricula').text
    #out['uf'] = element.find('uf').text
    out['telefone'] = element.find('fone').text
    out['url_foto'] = element.find('urlFoto').text
    out['legislatura'] = element_detalhes.find('numLegislatura').text
    out['email'] = element_detalhes.find('email').text
    out['profissao'] = element_detalhes.find('nomeProfissao').text
    out['data_nascimento'] = element_detalhes.find('dataNascimento').text
    out['data_falecimento'] = element_detalhes.find('dataFalecimento').text
    out['uf_representacao'] = element_detalhes.find('ufRepresentacaoAtual').text
    out['situacao'] = element_detalhes.find('situacaoNaLegislaturaAtual').text
    out['id_deputado_federal_deprecated'] = element_detalhes.find('idParlamentarDeprecated').text
    out['nome_parlamentar'] = element_detalhes.find('nomeParlamentarAtual').text
    out['nome'] = element_detalhes.find('nomeCivil').text
    out['sexo'] = element_detalhes.find('sexo').text
    out['partido_sigla'] = element_detalhes.find('./partidoAtual/idPartido').text
    out['partido'] = element_detalhes.find('./partidoAtual/sigla').text
    out['partido_nome'] = element_detalhes.find('./partidoAtual/nome').text
    out['gabinete_numero'] = element_detalhes.find('gabinete/numero').text
    out['gabinete_anexo'] = element_detalhes.find('gabinete/anexo').text
    return out

