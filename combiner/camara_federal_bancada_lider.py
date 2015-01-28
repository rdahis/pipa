# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item
from sqlalchemy import Column, Integer, String, Unicode, DateTime

class CamaraFederalBancadaLider(DeclarativeBase):
	__tablename__ = "camara_federal_bancada_lider"
	id_deputado_federal = Column('id_deputado_federal', Integer)
	bancada_sigla = Column('bancada_sigla', String, primary_key=True)
	posicao = Column('posicao', String)

raw2orm_translation = {
	#'nome': 'nome',
	'nome': None,
	#'id_cadastro': 'id_deputado_federal',
	'ideCadastro': 'id_deputado_federal',
	#'partido': 'partido',
	'partido': None,
	#'uf': 'uf',
	'uf': None,
	#'posicao': 'posicao',
	'posicao': 'posicao',
	'bancada_sigla': 'bancada_sigla',
	'bancada_nome': None,
}


raw_data = ['camara_federal_bancada_lider']
def combine(data):
	data = data.camara_federal_bancada_lider
	for item in data:
		translated_item = transform_dict(item, raw2orm_translation) 
		sanitized_item = sanitize_item(translated_item)
		yield CamaraFederalBancadaLider(**sanitized_item)


