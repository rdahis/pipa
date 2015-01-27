# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalDeputado(DeclarativeBase):
	__tablename__ = "camara_federal_deputado"
	id_deputado_federal = Column(Integer, primary_key=True)
	e_id_deputado_federal_deprecated = Column('e_id_deputado_federal_deprecated', Integer)
	e_id_matricula = Column('e_id_matricula', Integer)
	e_id_cadastro = Column('e_id_cadastro', Integer)
	e_id_orcamento = Column('e_id_orcamento', Integer)
	id_uf = Column('id_uf', Integer)
	uf_representacao = Column('uf_representacao', String)
	nome = Column('nome', String)
	nome_parlamentar = Column('nome_parlamentar', String)
	legislatura = Column('legislatura', Integer)
	condicao = Column('condicao', String)
	situacao = Column('situacao', String)
	data_nascimento = Column('data_nascimento', String)
	data_falecimento = Column('data_falecimento', String)
	url_foto = Column('url_foto', String)
	id_partido = Column('id_partido', String)
	sexo = Column('sexo', String)
	profissao = Column('profissao', String)
	telefone = Column('telefone', String)
	gabinete_numero = Column('gabinete_numero', String)
	gabinete_anexo = Column('gabinete_anexo', String)
	email = Column('email', String)


MODIFIED_COLUMNS = {
	'id_deputado_federal': 'id_deputado_federal',
	'id_deputado_federal_deprecated': 'e_id_deputado_federal_deprecated',
	'id_cadastro': 'e_id_cadastro',
	'id_matricula': 'e_id_matricula',
	'id_uf': 'id_uf',
	'uf_representacao': 'uf_representacao',
	'nome': 'nome',
	'nome_parlamentar': 'nome_parlamentar',
	'legislatura': 'legislatura',
	'condicao': 'condicao',
	'situacao': 'situacao',
	'data_nascimento': 'data_nascimento',
	'data_falecimento': 'data_falecimento',
	'url_foto': 'url_foto',
	'id_partido': 'id_partido',
	'partido': None,
	'sexo': 'sexo',
	'profissao': 'profissao',
	'telefone': 'telefone',
	'gabinete_numero': 'gabinete_numero',
	'gabinete_anexo': 'gabinete_anexo',
	'email': 'email'
}

#f(item, RULES)


raw_data = ['camara_deputados']
def combine(data):
	data = data.camara_deputados
	for item in data:
		columns = get_columns(CamaraFederalDeputado)
		#TODO: transform this line below into a dict comprehension
		filtered_item = dict(filter(lambda (k,v): k in columns, item.items()))
		filtered_item = sanitize_item(filtered_item)
		yield CamaraFederalDeputado(**filtered_item)

def get_columns(cls):
	return cls.__table__.columns.keys()

def sanitize_item(item):
	def clean(v):
		if type(v) not in (str, unicode) : return v
		v = v.strip()
		return v if v != '' else None
	return { k:clean(v) for k,v in item.items()}

#funcao para pegar todas as colunas da classe. output uma lista
#funcao filter (que ja existe) pra filtrar caras que nao tao na chamada 1a funcao
#por ultimo, apos receber
