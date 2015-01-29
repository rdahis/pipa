# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item
from sqlalchemy import Column, Integer, String, Unicode, DateTime

class CamaraFederalBancada(DeclarativeBase):
	__tablename__ = "camara_federal_bancada"
	id_bancada = Column(Integer, primary_key=True)
	bancada_sigla = Column('bancada_sigla', String)
	bancada_nome = Column('bancada_nome', String)

class CamaraFederalDeputadoBancada(DeclarativeBase):
	__tablename__ = "camara_federal_deputado_bancada"
	id_deputado = Column('id_deputado', Integer, primary_key=True)
	id_bancada = Column('id_bancada', Integer, primary_key=True)
	posicao = Column('posicao', String)


raw2orm_translation = {
	#'nome': 'nome',
	'nome': None,
	#'id_cadastro': 'id_deputado_federal',
	'ideCadastro': None,
	#'partido': 'partido',
	'partido': None,
	#'uf': 'uf',
	'uf': None,
	#'posicao': 'posicao',
	'posicao': None,
	'bancada_sigla': 'bancada_sigla',
	'bancada_nome': 'bancada_nome',
}


raw_data = ['camara_federal_lider_bancada']
def combine(data, db):
	data = data.camara_federal_lider_bancada
	for item in data:
		translated_item = transform_dict(item, raw2orm_translation) 
		sanitized_item = sanitize_item(translated_item)
		yield CamaraFederalBancada(**sanitized_item)


