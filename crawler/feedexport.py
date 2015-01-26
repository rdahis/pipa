# -*- coding: utf-8 -*-

from scrapy.contrib.exporter import CsvItemExporter

class CSVExport(CsvItemExporter):
	def __init__(self, *args, **kwargs):
		args[0].truncate(0)
		CsvItemExporter.__init__(self,*args,**kwargs)
