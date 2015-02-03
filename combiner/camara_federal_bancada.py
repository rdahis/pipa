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
	id_deputado = Column('id_deputado', String, primary_key=True)
	id_bancada = Column('id_bancada', Integer, primary_key=True)
	posicao = Column('posicao', String)


raw_data = ['camara_federal_bancada_lider']
def combine(data, db):
	data = data.camara_federal_bancada_lider
	last_bancada_sigla = None
	for item in data:
		item = sanitize_item(item)
		#TODO: converter esse if para dados estruturados em json e so pegar os titulos
		if last_bancada_sigla != item['bancada_sigla']:
			last_bancada_sigla = item['bancada_sigla']
			bancada = CamaraFederalBancada(
				bancada_sigla=item['bancada_sigla'],
				bancada_nome=item['bancada_nome'],
				)
			yield bancada
		deputado_bancada = CamaraFederalDeputadoBancada(
			id_deputado=item['ideCadastro'].encode(),
			id_bancada=bancada.id_bancada,
			posicao=item['posicao']
			)
		yield deputado_bancada

