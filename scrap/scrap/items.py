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

class ProjetoDeLei(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	ementa = Field()
	autores = Field()
	corpo = Field()


class DeputadoFederal(scrapy.Item):
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


