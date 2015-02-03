# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey



class VagasEleicao(DeclarativeBase):
	__tablename__ = "vagas_eleicao"
