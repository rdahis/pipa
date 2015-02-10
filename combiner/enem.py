# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, sanitize_item, Commit
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class Aluno(DeclarativeBase):
	__tablename__ = "aluno"
	#__table_args__ = {'schema':'enem'}
	id_aluno = Column('id_aluno', BigInteger, primary_key=True)
	idade = Column('idade', Integer)
	sexo = Column('sexo', Enum('M', 'F', name='sexo'))
	situacao_ensino_medio = Column('situacao_ensino_medio', String)
	ano_concluiu_ensino_medio = Column('ano_concluiu_ensino_medio', Integer)
	estado_civil = Column('estado_civil', String)
	cor_raca = Column('cor_raca' ,String)

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


raw_data = ['dados_enem_2012']
def combine(data, db):
	data = data.dados_enem_2012
	counter = 0
	for item in data:
		counter +=1
		if counter % 1000 == 0: yield Commit
		aluno = Aluno(
			id_aluno=item['NU_INSCRICAO'],
			idade=item['IDADE'],
			sexo= 'M' if item['TP_SEXO'] == '0' else 'F',
			situacao_ensino_medio=item['ST_CONCLUSAO'],
			ano_concluiu_ensino_medio= item['ANO_CONCLUIU'] if item['ANO_CONCLUIU'].isdigit() else None,
			estado_civil=item['TP_ESTADO_CIVIL'],
			cor_raca=item['TP_COR_RACA'],
		)
		aplicacao = __aplicacao(item, aluno)
		yield aplicacao

def __aplicacao(item, aluno):
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
	)


def __presenca(item,sub):
	pres = int(item[sub])
	if pres == 0: return 'Faltou'
	if pres == 1: return 'Presente'
	if pres == 2: return 'Eliminado'
	raise Exception('invalid presenca %s' % pres)

# IN_MESA_CADEIRA_RODAS': u'0', u'COD_MUNICIPIO_INSC': u'2933307', u'NU_NT_CN': u'.', u'COD_MUNICIPIO_PROVA': u'2933307', u'TX_RESPOSTAS_CN': u'', u'IN_AMPLIADA': u'0', u'IN_TRANSCRICAO': u'0', u'TP_COR_RACA': u'3', u'IN_PRESENCA_LC': u'0', u'IN_LEDOR': u'0', u'NU_NOTA_COMP4': u'.', u'ID_PROVA_CH': u'.', u'TX_RESPOSTAS_MT': u'', u'UF_INSC': u'BA', u'ID_PROVA_LC': u'.', u'IN_GESTANTE': u'0', u'IN_DEFICIENCIA_MENTAL': u'0', u'TP_ESCOLA': u'.', u'NU_NOTA_REDACAO': u'.', u'TP_LINGUA': u'.', u'IN_BRAILLE': u'0', u'NU_NT_LC': u'.', u'SIT_FUNC': u'.', u'TX_RESPOSTAS_CH': u'', u'DS_GABARITO_CH': u'', u'NO_ENTIDADE_CERTIFICACAO': u'', u'IN_PRESENCA_CH': u'0', u'IN_STATUS_REDACAO': u'F', u'NU_NT_MT': u'.', u'IN_ACESSO': u'0', u'IN_BAIXA_VISAO': u'0', u'IN_DEFICIENCIA_FISICA': u'0', u'IN_DISLEXIA': u'0', u'IN_LIBRAS': u'0', u'DS_GABARITO_MT': u'', u'ANO_CONCLUIU': u'2003', u'ST_CONCLUSAO': u'1', u'DS_GABARITO_CN': u'', u'NO_MUNICIPIO_INSC': u'VITORIA DA CONQUISTA', u'NU_INSCRICAO': u'400000000001', u'ID_DEPENDENCIA_ADM': u'.', u'IN_IDOSO': u'0', u'ID_LOCALIZACAO': u'.', u'UF_ENTIDADE_CERTIFICACAO': u'', u'IN_PRESENCA_CN': u'0', u'TX_RESPOSTAS_LC': u'', u'UF_ESC': u'', u'IN_LEITURA_LABIAL': u'0', u'NU_NOTA_COMP5': u'.', u'PK_COD_ENTIDADE': u'.', u'DS_GABARITO_LC': u'', u'NU_NOTA_COMP1': u'.', u'NO_MUNICIPIO_ESC': u'', u'NU_NOTA_COMP3': u'.', u'NU_NOTA_COMP2': u'.', u'IN_DEFICIT_ATENCAO': u'0', u'NO_MUNICIPIO_PROVA': u'VITORIA DA CONQUISTA', u'TP_ESTADO_CIVIL': u'1', u'IN_PRESENCA_MT': u'0', u'IN_APOIO_PERNA': u'0', u'ID_PROVA_CN': u'.', u'COD_MUNICIPIO_ESC': u'.', u'IN_LACTANTE': u'0', u'IN_SABATISTA': u'0', u'IN_GUIA_INTERPRETE': u'0', u'UF_MUNICIPIO_PROVA': u'BA', u'ID_PROVA_MT': u'.', u'IDADE': u'40', u'IN_DEFICIENCIA_AUDITIVA': u'0', u'IN_UNIDADE_HOSPITALAR': u'0', u'IN_AUTISMO': u'0', u'IN_SURDEZ': u'0', u'IN_TP_ENSINO': u'1', u'NU_ANO': u'2012', u'IN_CERTIFICADO': u'0', u'IN_MESA_CADEIRA_SEPARADA': u'0', u'TP_SEXO': u'0', u'IN_SURDO_CEGUEIRA': u'0', u'NU_NT_CH': u'.', u'IN_CEGUEIRA': u'0'}

