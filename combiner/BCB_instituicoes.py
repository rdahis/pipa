# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey


class InstituicaoBCB(DeclarativeBase):
	__tablename__ = 'BCB_instituicoes'
	id_instituicao = Column('id_instituicao', Integer, primary_key=True)
	instituicao = Column('instituicao', String)


raw2orm_translation = {

}


raw_data = [BCB_instituicoes]
def combine(data, db):
	data = data.BCB_instituicoes
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		candidato = InstituicaoBCB(**translated_item)
		yield candidato
