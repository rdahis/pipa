from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
	""" Performs database connection using database settings from settings.py.
	Returns sqlalchemy engine instance """
	return create_engine(URL(**settings.DATABASE))

def create_all_tables(engine):
	DeclarativeBase.metadata.create_all(engine)
