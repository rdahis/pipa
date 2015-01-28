# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalDeputado(DeclarativeBase):
	__tablename__ = "camara_federal_deputado"
	id_deputado_federal = Column(Integer, primary_key=True)
	e_id_deputado_federal_deprecated = Column('e_id_deputado_federal_deprecated', Integer)
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
	id_partido = Column('id_partido', String)
	sexo = Column('sexo', String)
	profissao = Column('profissao', String)
	telefone = Column('telefone', String)
	gabinete_numero = Column('gabinete_numero', String)
	gabinete_anexo = Column('gabinete_anexo', String)
	email = Column('email', String)


raw2orm_translation = {
	'idParlamentar': 'id_deputado_federal',
	'ideCadastro': 'id_deputado_federal',
	'idParlamentarDeprecated': 'e_id_deputado_federal_deprecated',
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
	'idPartido': 'id_partido',
	'sigla': None,
	'nome': None,
	'sexo': 'sexo',
	'nomeProfissao': 'profissao',
	'fone': 'telefone',
	'numero': 'gabinete_numero',
	'anexo': 'gabinete_anexo',
	'email': 'email'
}

# Partidos
row2orm_translation3 = {
	'idPartido': 'id_partido',
	'siglaPartido': 'partido_sigla',
	'nomePartido': 'partido_nome',
	'dataCriacao': 'partido_data_criacao',
	'dataExtincao': 'partido_data_extincao',
}

# Orgaos Cargos
raw2orm_translation4 = {
	'id': 'id_cargo',
	'descricao': 'cargo_descricao'
}

# Orgaos 
raw2orm_translation5 = {
	'id': 'id_orgao',
	'descricao': 'orgao_descricao'
}

raw_data = ['camara_federal_deputados']
def combine(data, db):
	data = data.camara_deputados
	for item in data:
		translated_item = transform_dict(item, raw2orm_translation) 
		sanitized_item = sanitize_item(translated_item)
		yield CamaraFederalDeputado(**sanitized_item)
