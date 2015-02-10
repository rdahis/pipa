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

def get_columns(cls):
	return cls.__table__.columns.keys()

def sanitize_item(item):
	def clean(v):
		if type(v) not in (str, unicode) : return v
		v = v.strip()
		return v if v != '' else None
	return { k:clean(v) for k,v in item.items()}

class Commit(object): pass

def get_or_create(db, cls, **kwargs):
	instance = db.query(cls).filter_by(**kwargs).first()
	if instance:
		return instance
	else:
		instance = cls(**kwargs)
		return instance
