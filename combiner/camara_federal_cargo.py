# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalCargo(DeclarativeBase):
	__tablename__ = "camara_federal_cargo"
	id_cargo = Column(Integer, primary_key=True)
	descricao = Column('descricao', String)


raw_data = ['camara_orgaos_cargos']
def combine(data):
	data = data.camara_orgaos_cargos
	for item in data:
		yield CamaraFederalCargo(**item)
