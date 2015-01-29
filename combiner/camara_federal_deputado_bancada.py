# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalDeputadoBancada(DeclarativeBase):
	__tablename__ = "camara_federal_deputado_bancada"
	id_deputado = Column('id_deputado', Integer, primary_key=True)
	id_bancada = Column('id_bancada', Integer, primary_key=True)
	posicao = Column('posicao', String)

raw2orm_translation = {
	'nome': None,
	'ideCadastro': 'id_deputado',
	'partido': None,
	'uf': None,
	'posicao': 'posicao',
	'bancada_sigla': None,
	'bancada_nome': None
}

combiners_needed = ['camara_federal_bancada']
raw_data = ['camara_federal_lider_bancada']
def combine(data, db):
	data = data.camara_federal_lider_bancada
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		yield CamaraFederalPartido(**translated_item)
