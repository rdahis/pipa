# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class CreditoTxJurosBCB():
	__tablename__ = 'BCB_txcredito_txjuros'
	#id_instituicao = Column('id_instituicao', Integer, primary_key=True)
	posicao = Column('posicao', Integer)
	instituicao = Column('instituicao', String)
	data = Column('data', String)
	segmento = Column('segmento', String)
	tipo_de_encargo = Column('tipo_de_encargo', String)
	modalidade = Column('modalidade', String)
	tx_juros_am = Column('tx_juros_am', Integer)
	tx_juros_aa = Column('tx_juros_aa', Integer)


raw2orm_translation = {

}


raw_data = [BCB_txcredito_txjuros]
def combine(data, db):
	data = data.BCB_txcredito_txjuros
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		credito_juros = CreditoTxJurosBCB(**translated_item)
		yield credito_juros
