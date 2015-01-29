# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field
from scrapy.http import HtmlResponse

class TestSpider(scrapy.Spider):
	name = "test"
	output_format = 'jsonlines'
	allowed_domains = ["www.google.com"]
	start_urls = (
		'http://www.google.com',
	)

	def parse(self, response):
		ci = ComplexItem()
		ci['plain'] = "fredf"
		ci['complex'] = {5:6, 7:{'fred':3}}
		yield ci
		yield ci

class ComplexItem(scrapy.Item):
	plain = Field()
	complex = Field()
