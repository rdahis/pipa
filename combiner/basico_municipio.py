# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class BaseMunicipio(DeclarativeBase):
	__tablename__ = "base_municipio"
	id = Column('', )
	id_ibge = Column('', )
	id_tse = Column('', )
	id_siafi = Column('', )
	ano = Column('', )
	municipio_ibge = Column('', )
	municipio_tse = Column('', )
	municipio_siafi = Column('', )


