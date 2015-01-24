# -*- coding: utf-8 -*-

from combiner.engine import DeclarativeBase

class CamaraFederalCargo(DeclarativeBase):
    __tablename__ = "camara_federal_cargo"
    id_cargo = Column(Integer, primary_key=True)
    descricao = Column('descricao', String)


raw_data = ['camara_orgaos_cargos']
def combine(cls, data):
    data = data['camara_orgaos_cargos']
    for item in data:
        yield CamaraFederalCargo(**item)
