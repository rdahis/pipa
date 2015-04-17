# -*- coding: utf-8 -*-

from combiner.util import DeclarativeBase, transform_dict, get_columns, sanitize_item
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from combiner.camara_federal_partido import CamaraFederalPartido
import datetime


class CNJ_MagistradoMesServentiaMunicipio(DeclarativeBase):
	__tablename__ = "CNJ_magistrado_mes_serventia_municipio"
	id_magistrado = Column('id_magistrado', Integer, primary_key=True)
	id_mes = Column('id_mes', Integer, primary_key=True)
	id_serventia = Column('id_serventia', Integer, primary_key=True)
	id_municipio = Column('id_municipio', Integer, primary_key=True)
	denuncias_queixas = Column('denuncias_queixas', Integer)
	despachos = Column('despachos', Integer)
	decisoes = Column('decisoes', Integer)
	sent_com_julg_merito = Column('sent_com_julg_merito', Integer)
	sent_sem_julg_merito = Column('sent_sem_julg_merito', Integer)
	sent_homol_acordos = Column('sent_homol_acordos', Integer)
	suspeicoes = Column('suspeicoes', Integer)
	sessao_juri = Column('sessao_juri', Integer)
	audiencias_marcadas = Column('audiencias_marcadas', Integer)
	audiencias_realizadas = Column('audiencias_realizadas', Integer)
	sent_extincao_punibilidade = Column('sent_extincao_punibilidade', Integer)
	redistribuidos = Column('redistribuidos', Integer)
	audiencias_remarcadas = Column('audiencias_remarcadas', Integer)
	autos_sent_100d = Column('autos_sent_100d', Integer)
	autos_ato_judicial = Column('autos_ato_judicial', Integer)
	despachos_plantao_judicial = Column('despachos_plantao_judicial', Integer)

class CNJ_Magistrado(DeclarativeBase):
	__tablename__ = "CNJ_magistrado"
	id_magistrado = Column(Integer, primary_key=True)
	magistrado_nome = Column('magistrado_nome', String)
	magistrado_tipo = Column('magistrado_tipo', String)

class CNJ_Mes(DeclarativeBase):
	__tablename__ = "CNJ_mes"
	id_mes = Column(Integer, primary_key=True)
	mes = Column('mes', Integer)

class CNJ_Serventia(DeclarativeBase):
	__tablename__ = "CNJ_serventia"
	id_serventia = Column(Integer, primary_key=True)
	serventia = Column('serventia', String)
	serventia_tipo = Column('serventia_tipo', String)
	competencia = Column('competencia', String)
	responsavel = Column('responsavel', String)
	telefone = Column('telefone', String)
	email = Column('email', String)
	servidores_concursados = Column('servidores_concursados', Integer)
	servidores_cedidos = Column('servidores_cedidos', Integer)
	servidores_em_exercicio = Column('servidores_em_exercicio', Integer)
	servidores_afastados = Column('servidores_afastados', Integer)
	funcionarios_terceirizados = Column('funcionarios_terceirizados', Integer)
	funcionarios_outros = Column('funcionarios_outros', Integer)
	forca_trabalho_atualizacao = Column('forca_trabalho_atualizacao', Integer)
	acervo = Column('acervo', Integer)
	distribuidos = Column('distribuidos', Integer)
	tombados = Column('tombados', Integer)
	comprimento100 = Column('comprimento100', Integer)
	andamento100 = Column('andamento100', Integer)
	inqueritos_policiais = Column('inqueritos_policiais', Integer)
	termos_circunstanciados = Column('termos_circunstanciados', Integer)
	arquivados = Column('arquivados', Integer)
	arquivamento_provisorio = Column('arquivamento_provisorio', Integer)
	precatorias = Column('precatorias', Integer)
	precatorias_devolvidas = Column('precatorias_devolvidas', Integer)
	remetidos_aos_tribunais = Column('remetidos_aos_tribunais', Integer)
	execucao_fiscal_sobrestados = Column('execucao_fiscal_sobrestados', Integer)
	audiencias_marcadas = Column('audiencias_marcadas', Integer)
	audiencias_realizadas = Column('audiencias_realizadas', Integer)

class CNJ_Municipio(DeclarativeBase):
	__tablename__ = "CNJ_municipio"
	id_municipio = Column('id_municipio', primary_key=True) #pegar id_ibge
	municipio_cnj = Column('municipio_cnj', String)
	e_id_uf = Column('e_id_uf', Integer)
	uf = Column('uf', String)



combiners_needed = ['']
raw_data = ['']
def combine(data, db):
	data = data.CNJ_magistrado_mes_serventia_municipio
	for item in data:
		item = satinize(item)
		magistrado = CNJ_MagistradoMesServentiaMunicipio(
			# preencher aqui com o dict com nomes das variaveis que vierem dos raws
		)
		
		magistrado = CNJ_Magistrado(
		)
		mes = CNJ_Mes(
		)
		serventia = CNJ_Serventia(
		)

		id_municipio = db.query().filter_by().all()
		municipio = CNJ_Municipio(
		)


	for item in data:
		item = sanitize_item(item)
		translated_item = transform_dict(item, raw2orm_translation) 
		deputado = CamaraFederalDeputado(**translated_item)
		yield deputado
		partido = db.query(CamaraFederalPartido).filter_by(e_id_partido=item['idPartido']).all()
		if partido:
			assert len(partido) == 1
			partido = partido[0]
			deputado_partido = CamaraFederalDeputadoPartido(
				id_deputado=deputado.id_deputado,
				id_partido=partido.id_partido,
				data_ingresso=datetime.date.today()
			)
			yield deputado_partido




