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

class CamaraFederalOrgaoNumerador(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_orgao_numerador"
	id_orgao_numerador = Column('id_orgao_numerador', Integer, primary_key=True)
	orgao_numerador_sigla = Column('orgao_numerador_sigla', String)
	orgao_numerador_nome = Column('orgao_numerador_nome', String)

class CamaraFederalRegime(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_regime"
	id_regime = Column('id_regime', Integer, primary_key=True)
	regime_texto = Column('regime_texto', String)

class CamaraFederalApreciacao(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_apreciacao"
	id_apreciacao = Column('id_apreciacao', Integer, primary_key=True)
	apreciacao_texto = Column('apreciacao_texto', String)

class CamaraFederalSituacao(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_situacao"
	id_situacao = Column('id_situacao', Integer, primary_key=True)
	situacao_descricao = Column('situacao_descricao', String)

class CamaraFederalOrgao(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_orgao"
	id_orgao = Column('id_orgao', Integer, primary_key=True)
	orgao_sigla = Column('orgao_sigla', String)

class CamaraFederalProposicaoPrincipal(DeclarativeBase):
	__tablename__ = "camara_federal_proposicao_principal"
	id_proposicao_principal = Column('id_proposicao_principal', Integer, primary_key=True)
	proposicao_principal = Column('proposicao_principal', String)


# Proposicoes
raw2orm_translation = {
	'id': 'id_proposicao',
	'nome': 'nome',
	'tipoProposicao_id': 'id_proposicao_tipo',
	'tipoProposicao_sigla': None,
	'tipoProposicao_nome': None,
	'numero': 'numero',
	'ano': 'ano',
	'orgaoNumerador_id': 'id_orgao',
	'orgaoNumerador_sigla': None,
	'orgaoNumerador_nome': None,
	'dataApresentacao': 'data_apresentacao',
	'txtEmenta': 'ementa_texto',
	'txtExplicacaoEmenta': 'ementa_texto_explicacao',
	'codRegime': 'id_regime',
	'txtRegime': None,
	'apreciacao_id': 'id_apreciacao',
	'apreciacao_txtApreciacao': None,
	'txtNomeAutor': None,
	'ideCadastro': 'id_deputado_federal',
	'codPartido': None,
	'txtSiglaPartido': None,
	'txtSiglaUF': None,
	'qtdeAutores': 'autores_qtd',
	'datDespacho': 'despacho_data',
	'txtDespacho': None,
	'situacao_id': 'id_situacao',
	'situacao_descricao': None,
	'codOrgaoEstado': 'id_orgao',
	'siglaOrgaoEstado': None,
	'codProposicaoPrincipal': 'id_proposicao_principal',
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

		proposicao = CamaraFederalProposicao(**translated_item)
		yield proposicao
		proposicao_tipo = CamaraFederalProposicaoTipo(
			proposicao_tipo_sigla=item['tipoProposicao_sigla'],
			proposicao_tipo_nome=item['tipoProposicao_nome']
			)
		yield proposicao_tipo
		orgao_numerador = CamaraFederalOrgaoNumerador(
			orgao_numerador_sigla=item['orgaoNumerador_sigla'],
			orgao_numerador_nome=item['orgaoNumerador_nome']
			)
		yield orgao_numerador
		regime = CamaraFederalRegime(
			id_regime=item['codRegime'],
			regime_texto=item['txtRegime']
			)
		if not db.query(CamaraFederalRegime).get(regime.id_regime):
			yield regime
		apreciacao = CamaraFederalApreciacao(
		 	id_apreciacao=item['apreciacao_id'],
			apreciacao_texto=item['apreciacao_txtApreciacao']
			)
		if not db.query(CamaraFederalApreciacao).get(apreciacao.id_apreciacao):
			yield apreciacao
		situacao = CamaraFederalSituacao(
		 	id_situacao=item['situacao_id'],
			situacao_descricao=item['situacao_descricao']
			)
		if situacao.id_situacao and not db.query(CamaraFederalSituacao).get(situacao.id_situacao):
			yield situacao
		orgao = CamaraFederalOrgao(
		 	id_orgao=item['codOrgaoEstado'],
			orgao_sigla=item['siglaOrgaoEstado']
			)
		#XXX-JSON when we have json we should update this to if orgao
		if orgao.id_orgao and not db.query(CamaraFederalOrgao).get(orgao.id_orgao):
			yield orgao
		proposicao_principal = CamaraFederalProposicaoPrincipal(
			id_proposicao_principal=item['codProposicaoPrincipal'],
			proposicao_principal=item['proposicaoPrincipal']	
			)
		if proposicao_principal.id_proposicao_principal != '0' and not db.query(CamaraFederalProposicaoPrincipal).get(proposicao_principal.id_proposicao_principal):
			yield proposicao_principal

