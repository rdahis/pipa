# -*- coding: utf-8 -*-
import scrapy
import scrap.items as items
from urlparse import urlparse

class ProjetosDeLeiRjSpider(scrapy.Spider):
	name = "projetos_de_lei_rj"
	allowed_domains = ["mail.camara.rj.gov.br"]
	start_urls = (
			'http://mail.camara.rj.gov.br/APL/Legislativos/scpro1316.nsf/Internet/LeiInt?OpenForm&Start=1&Count=1000',
			)

	def parse(self, response):
		for line in response.css('body>form>table')[1].css('tr'):
			if line.css('img[alt*="Red right arrow Icon"]'):
				url = line.css('a').xpath('@href')[0].extract()
				base = urlparse(response.url)
				yield scrapy.Request(base_url(base, url), callback=self.parse_law_page)
				break

	def parse_law_page(self, response):
		lei = items.ProjetoDeLei()
		import ipdb; ipdb.set_trace()
		lei['ementa'] = response.text
		yield lei

def base_url(base, uri):
	return base.scheme + '://' + base.netloc + uri
