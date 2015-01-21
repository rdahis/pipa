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
    id_cadastro = Field()
    id_deputado_federal = Field()
    id_orcamento = Field()
    nome = Field()
    nome_parlamentar = Field()
    sexo = Field()
    partido = Field()
    uf = Field()
    condicao = Field()
    matricula = Field()
    gabinete = Field()
    anexo = Field()
    telefone = Field()
    url_foto = Field()

class LiderBancada(scrapy.Item):
    nome = Field()
    id_cadastro = Field()
    partido = Field()
    uf = Field()

class PartidoCamara(scrapy.Item):
    id_partido_camara = Field()
    partido = Field()
    partido_nome = Field()
    partido_data_criacao = Field()
    partido_data_extincao = Field()

class OrgaoCargoCamara(scrapy.Item):
    id_cargo = Field()
    descricao = Field()

class OrgaoCamara(scrapy.Item):
    id_orgao = Field()
    descricao = Field()

#---------------------------------------#
# Camara de Vereadores - Rio de Janeiro
#---------------------------------------#

class ProjetoDeLei(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	ementa = Field()
	autores = Field()
	corpo = Field()

#Cargos

#Proposicoes

#Sessoes/Reunioes
#    Lista Presenca Parlamentares (DataIni, DataFim, matricula)







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


