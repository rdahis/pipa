# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalCargo(DeclarativeBase):
	__tablename__ = "camara_federal_cargo"
	id_cargo = Column(Integer, primary_key=True)
	descricao = Column('descricao', String)


raw_data = ['camara_federal_cargo']
def combine(data, db):
	for item in data.camara_federal_cargo:
		yield CamaraFederalCargo(**item)
