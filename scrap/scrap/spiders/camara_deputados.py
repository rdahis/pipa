# -*- coding: utf-8 -*-
import scrapy
import scrap.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class CamaraDeputadosSpider(scrapy.Spider):
    name = "camara_deputados"
    allowed_domains = ["www2.camara.leg.br/"]
    start_urls = (
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados',
    )

    def parse(self, response):
        tree = ET.fromstring(response.body)
        for deputado in tree.getchildren():
            d = _create_item_from_element(deputado)
            yield d

def _create_item_from_element(element):
    d = items.DeputadoCamara()
    d['id_cadastro'] = element.find('ideCadastro')
    d['id_deputado_federal'] = element.find('idParlamentar').text
    d['id_orcamento'] = element.find('codOrcamento').text
    d['nome'] = element.find('nome').text
    d['nome_parlamentar'] = element.find('nomeParlamentar').text
    d['sexo'] = element.find('sexo').text
    d['partido'] = element.find('partido').text
    d['uf'] = element.find('uf').text
    d['condicao'] = element.find('condicao').text
    d['matricula'] = element.find('matricula').text
    d['gabinete'] = element.find('gabinete').text
    d['anexo'] = element.find('anexo').text
    d['telefone'] = element.find('fone').text
    d['url_foto'] = element.find('urlFoto').text

