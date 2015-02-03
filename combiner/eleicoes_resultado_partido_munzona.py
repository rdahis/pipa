# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class ResultadosPartidoMunzonaEleicao(DeclarativeBase):
	__tablename__ = "eleicao_resultados_partido_munzona"
	id_ibge = Column('id_ibge', Integer, primary_key=True)
	id_tse = Column('id_tse', Integer, primary_key=True)
	ano = Column('ano', Integer, primary_key=True)
	turno = Column('turno', Integer)
	cargo = Column('cargo', String)
	tipo = Column('', )
	coligacao = Column('', )
	partido = Column('', )
	votos_p = Column('', )
	votos_c = Column('', )
	coef = Column('', )
	coef_c = Column('', )
	eleitos_c = Column('', )
	eleitos_c_media = Column('', )


raw2orm_translation = {

}


raw_data = []
for year in range(1998,2016,2):
	raw_data.append('votacao_partido_munzona_' + str(year))
def combine(data, db):
	data = data.eleicao_resultados_partido_munzona
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		resultado_partido = ResultadosPartidoMunzonaEleicao(**translated_item)
		yield resultado_partido









