# -*- coding: utf-8 -*-
import scrapy
import scrap.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class LideresBancadasSpider(scrapy.Spider):
    name = "camara_deputados_lideres_bancadas"
    allowed_domains = ["www2.camara.leg.br/"]
    start_urls = (
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterLideresBancadas',
    )

    def parse(self, response):
        tree = ET.fromstring(response.body)
        import ipdb; ipdb.set_trace()
        for pessoa in tree.getchildren():
            i = _create_item_from_element(pessoa)
            yield i

def _create_item_from_element(element):
    out = items.LiderBancada()
    out['nome'] = element.find('nome')
    out['id_cadastro'] = element.find('ideCadastro')
    out['partido'] = element.find('partido')
    out['uf'] = element.find('uf')
