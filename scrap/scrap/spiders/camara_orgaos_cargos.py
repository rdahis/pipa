# -*- coding: utf-8 -*-
import scrapy
import scrap.items as items

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement


class CamaraOrgaosCargosSpider(scrapy.Spider):
    name = "camara_orgaos_cargos"
    allowed_domains = ["www2.camara.leg.br/"]
    start_urls = (
        'http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ListarCargosOrgaosLegislativosCD',
    )

    def parse(self, response):
        tree = ET.fromstring(response.body)
        for cargo in tree.getchildren():
            i = _create_item_from_element(cargo)
            yield i

def _create_item_from_element(element):
    out = items.OrgaoCargoCamara()
    out['id_cargo'] = element.attrib['id']
    out['descricao'] = element.attrib['descricao']
    return out
