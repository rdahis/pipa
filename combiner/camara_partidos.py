# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalPartido(DeclarativeBase):
	__tablename__ = "camara_federal_partido"
	id_partido = Column(Integer, primary_key=True)
	e_id_partido = Column('e_id_partido', String)
	partido_sigla = Column('partido_sigla', String)
	partido_nome = Column('partido_nome', String)
	partido_data_criacao = Column('partido_data_criacao', String)
	partido_data_extincao = Column('partido_data_extincao', String)

raw2orm_translation = {
	'idPartido': 'e_id_partido',
	'siglaPartido': 'partido_sigla',
	'nomePartido': 'partido_nome',
	'dataCriacao': 'partido_data_criacao',
	'dataExtincao': 'partido_data_extincao',
}


raw_data = ['camara_partidos']
def combine(data):
	data = data.camara_partidos
	for item in data:
		translated_item = transform_dict(item, raw2orm_translation) 
		sanitized_item = sanitize_item(translated_item)
		yield CamaraFederalPartido(**sanitized_item)

def get_columns(cls):
	return cls.__table__.columns.keys()

def sanitize_item(item):
	def clean(v):
		if type(v) not in (str, unicode) : return v
		v = v.strip()
		return v if v != '' else None
	return { k:clean(v) for k,v in item.items()}