# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class LegendaEleicao(DeclarativeBase):
	__tablename__ = "eleicao_legenda"
	id_ibge = Column('id_ibge', Integer, primary_key=True)
	id_tse = Column('id_tse', Integer, primary_key=True)
	ano = Column('ano', Integer, primary_key=True)
	turno = Column('', Integer)
	cargo = Column('', String)
	tipo = Column('', Integer)
	partido = Column('', String, primary_key=True)
	coligacao = Column('', String)


raw2orm_translation = {

}


raw_data = []
for year in range(1998,2016,2):
	raw_data.append('consulta_legendas_' + str(year))
def combine(data, db):
	data = data.eleicao_legenda
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		legenda = LegendaEleicao(**translated_item)
		yield legenda




