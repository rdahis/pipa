
from combiner.util import DeclarativeBase, transform_dict
from sqlalchemy import Column, Integer, String, DateTime

class CamaraFederalSessao(DeclarativeBase):
	__table_name__ = "camara_federal_sessao"
	e_id_matricula = Column('e_id_matricula', Integer)
	sessao_inicio = Column('sessao_inicio', String)
	sessao_descricao = Column('sessao_descricao', String)



# Sessoes
raw2orm_translation = {
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



raw_data = ['camara_federal_sessao']
def combine(data, db):
	data = data.camara_federal_sessao
	for item in data:
		translated_item = transform_dict(item, raw2orm_translation) 
		sanitized_item = sanitize_item(translated_item)
		yield CamaraFederalSessao(**sanitized_item)
















