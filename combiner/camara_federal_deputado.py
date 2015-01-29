# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from combiner.camara_federal_partido import CamaraFederalPartido
import datetime

class CamaraFederalDeputado(DeclarativeBase):
	__tablename__ = "camara_federal_deputado"
	id_deputado = Column(Integer, primary_key=True)
	e_id_deputado_deprecated = Column('e_id_deputado_deprecated', Integer)
	e_id_matricula = Column('e_id_matricula', Integer)
	e_id_cadastro = Column('e_id_cadastro', Integer)
	id_orcamento = Column('id_orcamento', Integer)
	uf_representacao_atual = Column('uf_representacao_atual', String)
	nome = Column('nome', String)
	nome_parlamentar = Column('nome_parlamentar', String)
	legislatura = Column('legislatura', Integer)
	condicao = Column('condicao', String)
	situacao = Column('situacao', String)
	data_nascimento = Column('data_nascimento', String)
	data_falecimento = Column('data_falecimento', String)
	url_foto = Column('url_foto', String)
	sexo = Column('sexo', String)
	profissao = Column('profissao', String)
	telefone = Column('telefone', String)
	gabinete_numero = Column('gabinete_numero', String)
	gabinete_anexo = Column('gabinete_anexo', String)
	email = Column('email', String)


raw2orm_translation = {
	'idParlamentar': 'id_deputado',
	'idParlamentarDeprecated': 'e_id_deputado_deprecated',
	'ideCadastro': 'e_id_cadastro',
	'matricula': 'e_id_matricula',
	'codOrcamento': 'id_orcamento',
	'ufRepresentacaoAtual': 'uf_representacao_atual',
	'nomeCivil': 'nome',
	'nomeParlamentarAtual': 'nome_parlamentar',
	'numLegislatura': 'legislatura',
	'condicao': 'condicao',
	'situacaoNaLegislaturaAtual': 'situacao',
	'dataNascimento': 'data_nascimento',
	'dataFalecimento': 'data_falecimento',
	'urlFoto': 'url_foto',
	'idPartido': None,
	'sigla': None,
	'nome': None,
	'sexo': 'sexo',
	'nomeProfissao': 'profissao',
	'fone': 'telefone',
	'numero': 'gabinete_numero',
	'anexo': 'gabinete_anexo',
	'email': 'email'
}


combiners_needed = ['camara_federal_partido']
raw_data = ['camara_federal_deputado']
def combine(data, db):
	data = data.camara_federal_deputado
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		deputado = CamaraFederalDeputado(**translated_item)
		partido = db.query(CamaraFederalPartido).filter_by(e_id_partido=item['idPartido']).all()
		assert len(partido) == 1
		partido = partido[0]
		yield deputado
		yield CamaraFederalDeputadoPartido(id_deputado=deputado.id_deputado, id_partido=partido.id_partido, data_ingresso=datetime.date.today())


class CamaraFederalDeputadoPartido(DeclarativeBase):
	__tablename__ = "camara_federal_deputado_partido"
	id_deputado = Column(Integer, ForeignKey(CamaraFederalDeputado.id_deputado), primary_key=True)
	id_partido = Column(Integer, ForeignKey(CamaraFederalPartido.id_partido), primary_key=True)
	data_ingresso = Column('data_ingresso', Date, primary_key=True)

class CamaraFederalDeputadoCondicao(DeclarativeBase):
	__tablename__ = "camara_federal_deputado_condicao"
	id_deputado = Column(Integer, ForeignKey(CamaraFederalDeputado.id_deputado), primary_key=True)
	id_condicao = Column(Integer, ForeignKey(CamaraFederalCondicao.id_condicao), primary_key=True)
	data_mudanca = Column('data_mudanca', Date, primary_key=True)
