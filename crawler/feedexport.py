# -*- coding: utf-8 -*-

from scrapy.contrib.exporter import CsvItemExporter, JsonLinesItemExporter

def CustomExporter(*args, **kwargs):
	extention = args[0].name.split('.')[-1]
	if extention == 'csv':
		return CsvItemExporter(*args, **kwargs)
	elif extention == 'jsonlines':
		return JsonLinesItemExporter(*args, **kwargs)
	else:
		raise Exception('format %s is not supported' % extention)


from scrapy.contrib.feedexport import FileFeedStorage
class CustomFileFeedStorage(FileFeedStorage):
	def open(self, spider):
		try: output_format = spider.output_format
		except AttributeError: output_format = 'csv'
		self.path = self.path + '.' +  output_format
		return FileFeedStorage.open(self, spider)
