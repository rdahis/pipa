# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict
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


raw2orm_translation = {
	'ideCadastro': 'id_deputado_federal',
	'idParlamentarDeprecated': 'e_id_deputado_federal_deprecated',
	'ideCadastro': 'e_id_cadastro',
	'matricula': 'e_id_matricula',
	'uf': 'id_uf',
	'ufRepresentacao': 'uf_representacao',
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

# lideres bancadas
raw2orm_translation2 = {
	'nome': 'nome',
	'id_cadastro': 'e_id_cadastro',
	'partido': 'id_partido',
	'uf': 'uf',
	'posicao': 'posicao',
	'sigla': 'bancada',
	'nome': 'bancada_nome',
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

# Proposicoes
raw2orm_translation6 = {
	'id': 'id_proposicao',
	'nome': 'proposicao_nome',
	'tipoProposicao_id': 'e_id_tipo_proposicao',
	'tipoProposicao_sigla': 'proposicao_sigla_tipo',
	'tipoProposicao_nome': 'proposicao_nome_tipo',
	'numero': 'proposicao_numero',
	'ano': 'ano',
	'orgaoNumerador_id': 'e_id_orgao_numerador',
	'orgaoNumerador_sigla': 'orgao_numerador_sigla',
	'orgaoNumerador_nome': 'orgao_numerador_nome',
	'datApresentacao': 'data_apresentacao',
	'txtEmenta': 'ementa_texto',
	'txtExplicacaoEmenta': 'ementa_texto_explicacao',
	'codRegime': 'e_id_regime',
	'txtRegime': 'regime_texto',
	'apreciacao_id': 'e_id_apreciacao',
	'apreciacao_txtApreciacao': 'apreciacao_texto',
	'txtNomeAutor': 'autor_nome',
	'ideCadastro': 'e_id_cadastro',
	'codPartido': 'id_partido',
	'txtSiglaPartido': None,
	'txtSiglaUF': 'uf',
	'qtdAutores': 'autores_qtd',
	'datDespacho': 'despacho_data',
	'txtDespacho': 'despacho_texto',
	'situacao_id': 'id_situacao',
	'situacao_descricao': 'situacao_descricao',
	'codOrgaoEstado': 'id_orgao',
	'siglaOrgaoEstado': 'orgao_sigla',
	'codProposicaoPrincipal': 'id_proposicao_principal',
	'proposicaoPrincipal': 'proposicao_principal',
	'indGenero': 'ind_genero',
	'qtdOrgaosComEstado': 'orgaos_qtd'
}

# Sessoes
raw2orm_translation7 = {
	'carteiraParlamentar': "e_id_matricula",
	'nomeParlamentar': "parlamentar_nome_cheio",
	'siglaPartido': "id_partido",
	'siglaUF': "uf",
	'descricaoFrequenciaDia': "frequencia",
	'justificativa': "justificativa",
	'presencaExterna': "presenca_externa",
	'sessaoDia_inicio': "sessao_inicio",
	'sessaoDia_descricao': "sessao_descricao",
	'sessaoDia_frequencia': "sessao_frequencia"
}


raw_data = ['camara_deputados']
def combine(data):
	data = data.camara_deputados
	for item in data:
		#columns = get_columns(CamaraFederalDeputado)
		#TODO: transform this line below into a dict comprehension
		translated_item = transform_dict(item, raw2orm_translation) 
		#filtered_item = dict(filter(lambda (k,v): k in columns, item.items()))
		sanitized_item = sanitize_item(translated_item)
		yield CamaraFederalDeputado(**sanitized_item)

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
