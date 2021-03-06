# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class ResultadosCandidatoMunzonaEleicao(DeclarativeBase):
	__tablename__ = "eleicao_resultados_candidato_munzona"
	id_ibge = Column('id_ibge', Integer, primary_key=True)
	id_tse = Column('id_tse', Integer, primary_key=True)
	ano = Column('ano', Integer, primary_key=True)
	turno = Column('turno', Integer)
	seq_candidato = Column('seq_candidato', Integer)
	candidato = Column('candidato', String, primary_key=True)
	cargo = Column('cargo', String)
	situacao = Column('situacao', String)
	partido = Column('partido', String)
	votos = Column('votos', Integer)



raw2orm_translation = {

}


raw_data = []
for year in range(1998,2016,2):
	raw_data.append('votacao_candidato_munzona_' + str(year))
def combine(data, db):
	data = data.eleicao_resultados_candidato_munzona
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		resultado_candidato = ResultadosCandidatoMunzonaEleicao(**translated_item)
		yield resultado_candidato



