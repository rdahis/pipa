# -*- coding: utf-8 -*-

# Define your item pipelines here
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import db_connect, create_all_tables
import models

class ScrapPipeline(object):
	def __init__(self):
		engine = db_connect()
		create_all_tables(engine)
		self.Session = sessionmaker(bind=engine)

	def process_item(self, item, spider):
		try:
			klass = models.__dict__[type(item).__name__]
		except:
			print('item does not have an equivalent module')
			return item
		session = self.Session()
		db_item = klass(**item)
		try:
			session.add(db_item)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()
		return item
