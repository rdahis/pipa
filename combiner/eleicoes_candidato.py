# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class CandidatoEleicao(DeclarativeBase):
	__tablename__ = "eleicao_candidato"
	turno = Column('', Integer)
	cargo = Column('', String)
	candidato = Column('', String, primary_key=True)
	seq_candidato = Column('', Integer)
	partido = Column('', String)
	ocupacao = Column('', String)
	idade = Column('', Integer)
	titulo = Column('', String)
	sexo = Column('', String)
	instrucao = Column('', String)
	estado_civil = Column('', String)
	situacao = Column('', String)


raw2orm_translation = {

}


raw_data = []
for year in range(1998,2016,2):
	raw_data.append('consulta_cand_' + str(year))
def combine(data, db):
	data = data.eleicao_candidato
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		candidato = CandidatoEleicao(**translated_item)
		yield candidato























