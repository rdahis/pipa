from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

DATABASE = {
		'drivername': 'postgres',
		'host': 'localhost',
		'port': '5432',
		'username': 'vagrant',
		'password': '.',
		'database': 'DP'
}

DeclarativeBase = declarative_base()

def db_connect():
	# Nao to entendendo nada dessa merda, mas vambora
	engine = create_engine(URL(**DATABASE))
	create_all_tables(engine)
	return sessionmaker(bind=engine)()


def create_all_tables(engine):
	DeclarativeBase.metadata.create_all(engine)

def transform_dict(d, tr_rules):
	ret = {}
	for k,v in d.items():
		if tr_rules[k]:
			ret[tr_rules[k]] = v
	return ret
