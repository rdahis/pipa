# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class DetalhesVotacaoEleicao(DeclarativeBase):
	__tablename__ = "eleicao_detalhes_votacao"
	id_ibge = Column('id_ibge', Integer, primary_key=True)
	id_tse = Column('id_tse', Integer, primary_key=True)
	ano = Column('ano', Integer, primary_key=True)
	turno = Column('', )
	cargo = Column('', )
	aptos = Column('', )
	comparecimentos = Column('', )
	B_A = Column('', )
	abstencoes = Column('', )
	C_A = Column('', )
	votos_validos = Column('', )
	D_B = Column('', )
	votos_brancos = Column('', )
	E_B = Column('', )
	votos_nulos = Column('', )
	F_B = Column('', )
	votos_nulos_apurados = Column('', )
	G_B = Column('', )


raw2orm_translation = {

}


raw_data = []
for year in range(1998,2016,2):
	raw_data.append('detalhe_votacao_munzona_' + str(year))
def combine(data, db):
	data = data.eleicao_detalhes_votacao
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		detalhes_votacao = DetalhesVotacaoEleicao(**translated_item)
		yield detalhes_votacao




