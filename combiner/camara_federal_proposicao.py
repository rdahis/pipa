# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item
from sqlalchemy import Column, Integer, String, Unicode, DateTime

class CamaraFederalProposicao(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao"
	id_proposicao = Column('id_proposicao', Integer, primary_key=True)
	id_deputado_federal = Column('id_deputado_federal', Integer)
	nome = Column('nome', String)
	numero = Column('numero', Integer)
	ano = Column('ano', Integer)
	id_proposicao_tipo = Column('id_proposicao_tipo', Integer)
	data_apresentacao = Column('data_apresentacao', String)
	ementa_texto = Column('ementa_texto', String)
	ementa_texto_explicacao = Column('ementa_texto_explicacao', String)
	id_regime = Column('id_regime', Integer)
	autores_qtd = Column('autores_qtd', Integer)
	despacho_data = Column('despacho_data', String)
	#despacho_texto = Column('despacho_texto', Unicode)
	id_apreciacao = Column('id_apreciacao', Integer)
	id_situacao = Column('id_situacao', Integer)
	id_orgao = Column('id_orgao', Integer)
	id_proposicao_principal = Column('id_proposicao_principal',Integer)
	#ind_genero = Column('ind_genero', String)
	orgaos_qtd = Column('orgaos_qtd', Integer)

class CamaraFederalProposicaoTipo(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_tipo"
	id_proposicao_tipo = Column(Integer, primary_key=True)
	proposicao_tipo_sigla = Column('proposicao_tipo_sigla', String)
	proposicao_tipo_nome = Column('proposicao_tipo_nome', String)



# Proposicoes
raw2orm_translation = {
	'id': 'id_proposicao',
	'nome': 'nome',
	'tipoProposicao_id': 'id_proposicao_tipo',
	#'tipoProposicao_sigla': 'proposicao_tipo_sigla',
	'tipoProposicao_sigla': None,
	#'tipoProposicao_nome': 'proposicao_tipo_nome',
	'tipoProposicao_nome': None,
	#'numero': 'proposicao_numero',
	'numero': 'numero',
	'ano': 'ano',
	'orgaoNumerador_id': 'id_orgao',
	#'orgaoNumerador_sigla': 'orgao_numerador_sigla',
	'orgaoNumerador_sigla': None,
	#'orgaoNumerador_nome': 'orgao_numerador_nome',
	'orgaoNumerador_nome': None,
	'dataApresentacao': 'data_apresentacao',
	'txtEmenta': 'ementa_texto',
	'txtExplicacaoEmenta': 'ementa_texto_explicacao',
	'codRegime': 'id_regime',
	#'txtRegime': 'regime_texto',
	'txtRegime': None,
	'apreciacao_id': 'id_apreciacao',
	#'apreciacao_txtApreciacao': 'apreciacao_texto',
	'apreciacao_txtApreciacao': None,
	#'txtNomeAutor': 'autor_nome',
	'txtNomeAutor': None,
	'ideCadastro': 'id_deputado_federal',
	#'codPartido': 'id_partido',
	'codPartido': None,
	'txtSiglaPartido': None,
	#'txtSiglaUF': 'uf',
	'txtSiglaUF': None,
	'qtdeAutores': 'autores_qtd',
	'datDespacho': 'despacho_data',
	#'txtDespacho': 'despacho_texto',
	'txtDespacho': None,
	'situacao_id': 'id_situacao',
	#'situacao_descricao': 'situacao_descricao',
	'situacao_descricao': None,
	'codOrgaoEstado': 'id_orgao',
	#'siglaOrgaoEstado': 'orgao_sigla',
	'siglaOrgaoEstado': None,
	'codProposicaoPrincipal': 'id_proposicao_principal',
	#'proposicaoPrincipal': 'proposicao_principal',
	'proposicaoPrincipal': None,
	'indGenero': None,
	'qtdOrgaosComEstado': 'orgaos_qtd'
}


raw_data = ['camara_federal_proposicao']
def combine(data, db):
	data = data.camara_federal_proposicao
	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 

		yield CamaraFederalProposicaoTipo(
			proposicao_tipo_sigla=item['tipoProposicao_sigla'],
			proposicao_tipo_nome=item['tipoProposicao_nome']
			)

		yield CamaraFederalProposicao(**item)
