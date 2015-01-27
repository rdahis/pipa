# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


#----------------------------------------------------------------#
# Politics
#----------------------------------------------------------------#

#----------------------#
# Camara dos Deputados
#----------------------#

class DeputadoCamara(scrapy.Item):
	ideCadastro = Field()
	idParlamentar = Field()
	codOrcamento = Field()
	condicao = Field()
	matricula = Field()
	fone = Field()
	urlFoto = Field()
	numLegislatura = Field()
	email = Field()
	nomeProfissao = Field()
	dataNascimento = Field()
	dataFalecimento = Field()
	ufRepresentacaoAtual = Field()
	situacaoNaLegislaturaAtual = Field()
	idParlamentarDeprecated = Field()
	nomeParlamentarAtual = Field()
	nomeCivil = Field()
	sexo = Field()
	idPartido = Field()
	sigla = Field()
	nome = Field()
	numero = Field()
	anexo = Field()

class LiderBancada(scrapy.Item):
	nome = Field()
	id_cadastro = Field()
	partido = Field()
	uf = Field()
	posicao = Field()
	sigla = Field()
	nome = Field()

class PartidoCamara(scrapy.Item):
	idPartido = Field()
	siglaPartido = Field()
	nomePartido = Field()
	dataCriacao = Field()
	dataExtincao = Field()

class OrgaoCargoCamara(scrapy.Item):
	id = Field()
	descricao = Field()

class OrgaoCamara(scrapy.Item):
	id = Field()
	descricao = Field()

class ProposicaoCamara(scrapy.Item):
	id = Field()
	nome = Field()
	tipoProposicao_id = Field()
	tipoProposicao_sigla = Field()
	tipoProposicao_nome = Field()
	numero = Field()
	ano = Field()
	orgaoNumerador_id = Field()
	orgaoNumerador_sigla = Field()
	orgaoNumerador_nome = Field()
	dataApresentacao = Field()
	txtEmenta = Field()
	txtExplicacaoEmenta = Field()
	codRegime = Field()
	txtRegime = Field()
	apreciacao_id = Field()
	apreciacao_txtApreciacao = Field()
	txtNomeAutor = Field()
	ideCadastro = Field()
	codPartido = Field()
	txtSiglaPartido = Field()
	txtSiglaUF = Field()
	qtdeAutores = Field()
	datDespacho = Field()
	txtDespacho = Field()
	situacao_id = Field()
	situacao_descricao = Field()
	codOrgaoEstado = Field()
	siglaOrgaoEstado = Field()
	codProposicaoPrincipal = Field()
	proposicaoPrincipal = Field()
	indGenero = Field()
	qtdOrgaosComEstado = Field()

class PresencaSessaoDeputadoCamara(scrapy.Item):
	carteiraParlamentar = Field()
	nomeParlamentar = Field()
	siglaPartido = Field()
	siglaUF = Field()
	descricaoFrequenciaDia = Field()
	justificativa = Field()
	presencaExterna = Field()
	sessaoDia_inicio = Field()
	sessaoDia_descricao = Field()
	sessaoDia_frequencia = Field()






#---------------------------------------#
# Camara de Vereadores - Rio de Janeiro
#---------------------------------------#

class ProjetoDeLei(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	ementa = Field()
	autores = Field()
	corpo = Field()




#----------------------------------------------------------------#
# Government
#----------------------------------------------------------------#

#----------------------------------------------------------------#
# Economy
#----------------------------------------------------------------#

#----------------------------------------------------------------#
# Education
#----------------------------------------------------------------#

#----------------------------------------------------------------#
# Health
#----------------------------------------------------------------#

#----------------------------------------------------------------#
# Transportation
#----------------------------------------------------------------#


