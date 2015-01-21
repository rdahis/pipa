from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import settings

def db_connect():
	""" Performs database connection using database settings from settings.py.
	Returns sqlalchemy engine instance """
	return create_engine(URL(**settings.DATABASE))
