# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item, Commit, get_or_create
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class Aluno(DeclarativeBase):
	__tablename__ = "aluno"
	#__table_args__ = {'schema':'enem'}
	id_aluno = Column(BigInteger, primary_key=True)
	idade = Column(Integer)
	sexo = Column(Enum('M', 'F', name='sexo'))
	situacao_ensino_medio = Column(String)
	ano_concluiu_ensino_medio = Column(Integer)
	estado_civil = Column(String)
	cor_raca = Column(String)
	id_escola = Column(ForeignKey('escola.id_escola'))
	escola = relationship('Escola')
	id_municipio = Column(ForeignKey('municipio.id_municipio'))
	municipio = relationship('Municipio')

_Presenca = Enum('Faltou', 'Presente', 'Eliminado', name='presenca')
class Aplicacao(DeclarativeBase):
	__tablename__ = "aplicacao"
	aluno = relationship("Aluno", uselist=False)
	id_aluno = Column(ForeignKey('aluno.id_aluno'), primary_key=True)
	presenca_cn = Column(_Presenca)
	presenca_ch = Column(_Presenca)
	presenca_lc = Column(_Presenca)
	presenca_mt = Column(_Presenca)
	nota_cn = Column(String)
	nota_ch = Column(String)
	nota_lc = Column(String)
	nota_mt = Column(String)
	respostas_cn = Column(String)
	respostas_ch = Column(String)
	respostas_lc = Column(String)
	respostas_mt = Column(String)
	lingua_estrangeira = Column(String)
	status_redacao = Column(String)
	redacao_comp1 = Column(String)
	redacao_comp2 = Column(String)
	redacao_comp3 = Column(String)
	redacao_comp4 = Column(String)
	redacao_comp5 = Column(String)
	nota_redacao = Column(String)
	id_municipio = Column(ForeignKey('municipio.id_municipio'))
	municipio = relationship('Municipio')

class AlunoXNecessidadeEspecial(DeclarativeBase):
	__tablename__ = "aluno_x_necessidade_especial"
	id_aluno = Column(ForeignKey(Aluno.id_aluno), primary_key=True)
	id_necessidade_especial = Column(ForeignKey(
			'necessidade_especial.id_necessidade_especial'), primary_key=True)

class NecessidadeEspecial(DeclarativeBase):
	__tablename__ = "necessidade_especial"
	id_necessidade_especial = Column(Integer, primary_key=True)
	nome = Column(String)
	aluno = relationship(Aluno, secondary='aluno_x_necessidade_especial',
			backref="necessidade_especial")

_AdmnistracaoEscola = Enum('Federal', 'Estadual', 'Municipal', 'Privada', name='administracao_escola')
_ZonaEscola = Enum('Urbana', 'Rural', name='zona_escola')
_SituacaoEscola = Enum('Em Atividade', 'Paralisada', 'Extinta', 'Extinta em anos anteriores', name='situacao_escola')
class Escola(DeclarativeBase):
	__tablename__ = 'escola'
	id_escola = Column(Integer, primary_key=True)
	administracao = Column(_AdmnistracaoEscola)
	#tipo_instituicao = Column()
	zona = Column(_ZonaEscola)
	situacao = Column(_SituacaoEscola)
	id_municipio = Column(ForeignKey('municipio.id_municipio'))
	municipio = relationship('Municipio')

class Municipio(DeclarativeBase):
	__tablename__ = 'municipio'
	id_municipio = Column(Integer, primary_key=True)
	nome = Column(String)
	uf = Column(String)

raw_data = ['dados_enem_2012']
def combine(data, db):
	data = data.dados_enem_2012
	_create_necessidade_especiais()
	counter = 0
	for item in data:
		counter +=1
		if counter % 1000 == 0: yield Commit
		escola = _get_escola(db, item)
		aluno = Aluno(
			id_aluno=item['NU_INSCRICAO'],
			idade=item['IDADE'],
			sexo= 'M' if item['TP_SEXO'] == '0' else 'F',
			situacao_ensino_medio=item['ST_CONCLUSAO'],
			ano_concluiu_ensino_medio= item['ANO_CONCLUIU'] if item['ANO_CONCLUIU'].isdigit() else None,
			estado_civil=item['TP_ESTADO_CIVIL'],
			cor_raca=item['TP_COR_RACA'],
			escola=escola,
			municipio = __municipio(db, item, 'INSC'),
		)
		__add_necessidade_especial(item, aluno)
		aplicacao = __aplicacao(db, item, aluno)
		yield aplicacao

def _get_escola(db, item):
	if item['PK_COD_ENTIDADE'] == '.': return None
	return get_or_create(db, Escola,
		id_escola=item['PK_COD_ENTIDADE'],
		administracao=( {'1': 'Federal', '2':'Estadual', '3':'Municipal', '4':'Privada', '.':None}
				[item['ID_DEPENDENCIA_ADM']]),
		zona=( {'1':'Urbana', '2':'Rural', '.':None}[item['ID_LOCALIZACAO']]),
		situacao=( {'1':'Em Atividade', '2':'Paralisada', '3':'Extinta', '4':'Extinta em anos anteriores', '.':None}
				[item['SIT_FUNC']]),
		municipio = __municipio(db, item, 'ESC'),
	)

NECESSIDADES = {}

def __add_necessidade_especial(item, aluno):
	for k,v in NECESSIDADES.items():
		if item[k] == '1':
			aluno.necessidade_especial.append(v)

def _create_necessidade_especiais():
	NECESSIDADES_TRANSFORM = {
		'IN_UNIDADE_HOSPITALAR': 'unidade_hospitalar',
		'IN_BAIXA_VISAO': 'baixa_visao',
		'IN_CEGUEIRA': 'cegueira',
		'IN_SURDEZ': 'surdez',
		'IN_DEFICIENCIA_AUDITIVA': 'deficiencia_auditiva',
		'IN_SURDO_CEGUEIRA': 'surdo_cegueira',
		'IN_DEFICIENCIA_FISICA': 'deficiencia_fisica',
		'IN_DEFICIENCIA_MENTAL': 'deficiencia_mental',
		'IN_DEFICIT_ATENCAO': 'deficit_atencao',
		'IN_DISLEXIA': 'dislexia',
		'IN_GESTANTE': 'gestante',
		'IN_LACTANTE': 'lactante',
		'IN_IDOSO': 'idoso',
		'IN_AUTISMO': 'autismo',
		'IN_SABATISTA': 'sabatista',
		'IN_BRAILLE': 'braille',
		'IN_AMPLIADA': 'ampliada',
		'IN_LEDOR': 'ledor',
		'IN_ACESSO': 'acesso',
		'IN_TRANSCRICAO': 'transcricao',
		'IN_LIBRAS': 'libras',
		'IN_LEITURA_LABIAL': 'leitura_labial',
		'IN_MESA_CADEIRA_RODAS': 'mesa_cadeira_rodas',
		'IN_MESA_CADEIRA_SEPARADA': 'mesa_cadeira_separada',
		'IN_APOIO_PERNA': 'apoio_perna',
		'IN_GUIA_INTERPRETE': 'guia_interprete',
	}
	for k,v in NECESSIDADES_TRANSFORM.items():
		NECESSIDADES[k] = NecessidadeEspecial(nome=v)

def __aplicacao(db, item, aluno):
	return Aplicacao(
			presenca_cn=__presenca(item,'IN_PRESENCA_CN'),
			presenca_ch=__presenca(item,'IN_PRESENCA_CH'),
			presenca_lc=__presenca(item,'IN_PRESENCA_LC'),
			presenca_mt=__presenca(item,'IN_PRESENCA_MT'),
			nota_cn=item['NU_NT_CN'],
			nota_ch=item['NU_NT_CH'],
			nota_lc=item['NU_NT_LC'],
			nota_mt=item['NU_NT_MT'],
			respostas_cn=item['TX_RESPOSTAS_CN'],
			respostas_ch=item['TX_RESPOSTAS_CH'],
			respostas_lc=item['TX_RESPOSTAS_LC'],
			respostas_mt=item['TX_RESPOSTAS_MT'],
			lingua_estrangeira=item['TP_LINGUA'],
			status_redacao=item['IN_STATUS_REDACAO'],
			redacao_comp1=item['NU_NOTA_COMP1'],
			redacao_comp2=item['NU_NOTA_COMP2'],
			redacao_comp3=item['NU_NOTA_COMP3'],
			redacao_comp4=item['NU_NOTA_COMP4'],
			redacao_comp5=item['NU_NOTA_COMP5'],
			nota_redacao=item['NU_NOTA_REDACAO'],
			aluno=aluno,
			municipio = __municipio(db, item, 'PROVA')
	)

def __presenca(item, sub):
	pres = int(item[sub])
	if pres == 0: return 'Faltou'
	if pres == 1: return 'Presente'
	if pres == 2: return 'Eliminado'
	raise Exception('invalid presenca %s' % pres)

def __municipio(db, item, suffix):
	id_municipio = item['COD_MUNICIPIO_' + suffix]
	municipio = __municipio.cache.get(id_municipio)
	if municipio: return municipio
	nome = item['NO_MUNICIPIO_' + suffix]
	if suffix == 'PROVA':
		uf = item['UF_MUNICIPIO_PROVA']
	else:
		uf = item['UF_' + suffix]
	municipio = get_or_create(db, Municipio, id_municipio=id_municipio, nome=nome, uf=uf)
	__municipio.cache[id_municipio] = municipio
	return municipio
__municipio.cache = {}



# IN_MESA_CADEIRA_RODAS': u'0', u'COD_MUNICIPIO_INSC': u'2933307', u'NU_NT_CN': u'.', u'COD_MUNICIPIO_PROVA': u'2933307', u'TX_RESPOSTAS_CN': u'', u'IN_AMPLIADA': u'0', u'IN_TRANSCRICAO': u'0', u'TP_COR_RACA': u'3', u'IN_PRESENCA_LC': u'0', u'IN_LEDOR': u'0', u'NU_NOTA_COMP4': u'.', u'ID_PROVA_CH': u'.', u'TX_RESPOSTAS_MT': u'', u'UF_INSC': u'BA', u'ID_PROVA_LC': u'.', u'IN_GESTANTE': u'0', u'IN_DEFICIENCIA_MENTAL': u'0', u'TP_ESCOLA': u'.', u'NU_NOTA_REDACAO': u'.', u'TP_LINGUA': u'.', u'IN_BRAILLE': u'0', u'NU_NT_LC': u'.', u'SIT_FUNC': u'.', u'TX_RESPOSTAS_CH': u'', u'DS_GABARITO_CH': u'', u'NO_ENTIDADE_CERTIFICACAO': u'', u'IN_PRESENCA_CH': u'0', u'IN_STATUS_REDACAO': u'F', u'NU_NT_MT': u'.', u'IN_ACESSO': u'0', u'IN_BAIXA_VISAO': u'0', u'IN_DEFICIENCIA_FISICA': u'0', u'IN_DISLEXIA': u'0', u'IN_LIBRAS': u'0', u'DS_GABARITO_MT': u'', u'ANO_CONCLUIU': u'2003', u'ST_CONCLUSAO': u'1', u'DS_GABARITO_CN': u'', u'NO_MUNICIPIO_INSC': u'VITORIA DA CONQUISTA', u'NU_INSCRICAO': u'400000000001', u'ID_DEPENDENCIA_ADM': u'.', u'IN_IDOSO': u'0', u'ID_LOCALIZACAO': u'.', u'UF_ENTIDADE_CERTIFICACAO': u'', u'IN_PRESENCA_CN': u'0', u'TX_RESPOSTAS_LC': u'', u'UF_ESC': u'', u'IN_LEITURA_LABIAL': u'0', u'NU_NOTA_COMP5': u'.', u'PK_COD_ENTIDADE': u'.', u'DS_GABARITO_LC': u'', u'NU_NOTA_COMP1': u'.', u'NO_MUNICIPIO_ESC': u'', u'NU_NOTA_COMP3': u'.', u'NU_NOTA_COMP2': u'.', u'IN_DEFICIT_ATENCAO': u'0', u'NO_MUNICIPIO_PROVA': u'VITORIA DA CONQUISTA', u'TP_ESTADO_CIVIL': u'1', u'IN_PRESENCA_MT': u'0', u'IN_APOIO_PERNA': u'0', u'ID_PROVA_CN': u'.', u'COD_MUNICIPIO_ESC': u'.', u'IN_LACTANTE': u'0', u'IN_SABATISTA': u'0', u'IN_GUIA_INTERPRETE': u'0', u'UF_MUNICIPIO_PROVA': u'BA', u'ID_PROVA_MT': u'.', u'IDADE': u'40', u'IN_DEFICIENCIA_AUDITIVA': u'0', u'IN_UNIDADE_HOSPITALAR': u'0', u'IN_AUTISMO': u'0', u'IN_SURDEZ': u'0', u'IN_TP_ENSINO': u'1', u'NU_ANO': u'2012', u'IN_CERTIFICADO': u'0', u'IN_MESA_CADEIRA_SEPARADA': u'0', u'TP_SEXO': u'0', u'IN_SURDO_CEGUEIRA': u'0', u'NU_NT_CH': u'.', u'IN_CEGUEIRA': u'0'}

