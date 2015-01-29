# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalCondicao(DeclarativeBase):
	__tablename__ = "camara_federal_condicao"
	id_condicao = Column(Integer, primary_key=True)
	condicao = Column('condicao', String)

raw_data = ['camara_federal_deputado']
def combine(data, db):
	data = data.camara_federal_partido
	for item in data:
		item = sanitize_item(item)
		# inserir aqui as colunas do raw
		translated_item = transform_dict(item, raw2orm_translation) 
		yield CamaraFederalPartido(**sanitized_item)
