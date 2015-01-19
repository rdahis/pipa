
#-----------------------------------------------------------------#
#
#   Title: Crawler - Camara dos Deputados
#   Author: Ricardo Dahis
#   Last Update: 19/01/2015
#
#-----------------------------------------------------------------#


# System
import sys, os
# Pretty Print
import pprint

# XML Parser
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element, SubElement

# Postgresql Connection
import psycopg2
import psycopg2.extras

#from sqlalchemy import *
#from sqlalchemy.orm import *
#import sqlalchemy
#import sqlalchemy
#from sqlalchemy import * 
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker


def main():
    
    try:
        conn = psycopg2.connect(dbname="DP", user="ricardodahis", host="/tmp/")
    except:
        print "I'm not being able to connect to database."
    
    cur = conn.cursor()
    
    conn.set_isolation_level(0)
    cur.execute("DROP TABLE IF EXISTS deputados_federais")
    cur.execute(
            """CREATE TABLE deputados_federais(
            id_deputado_federal integer,
            nome varchar,
            sexo varchar,
            profissao varchar,
            legenda varchar,
            uf varchar,
            condicao varchar,
            situacao varchar,
            matricula varchar,
            gabinete varchar,
            anexo varchar,
            telefone varchar
            )"""
    )


# Data file
    tree = ET.parse("/Users/ricardodahis/Dropbox/dados-publicos/tmp/Camara/Deputados.xml")
    root = tree.getroot()

    for deputado in root.findall('./Deputados/Deputado'):
        
        d = DeputadoFederal()

        d.id_deputado_federal = deputado.find('ideCadastro').text
        d.nome = deputado.find('nomeParlamentar').text
        d.sexo = deputado.find('SEXO').text
        d.profissao = deputado.find('Profissao').text
        d.legenda = deputado.find('LegendaPartidoEleito').text
        d.uf = deputado.find('UFEleito').text
        d.condicao = deputado.find('Condicao').text
        d.situacao = deputado.find('SiTuacaoMandato').text
        d.matricula = deputado.find('Matricula').text
        d.gabinete = deputado.find('Gabinete').text
        d.anexo = deputado.find('Anexo').text
        d.telefone = deputado.find('Fone').text
        #print d

        cur.execute(
                """INSERT INTO deputados_federais
                (id_deputado_federal, nome, sexo, profissao, legenda, uf, condicao, situacao, matricula, gabinete, anexo, telefone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (d.id_deputado_federal, d.nome, d.sexo, d.profissao, d.legenda,
                    d.uf, d.condicao, d.situacao, d.matricula, d.gabinete, d.anexo, d.telefone)
        )


    cur.execute("SELECT * FROM deputados_federais")
    #records = cur.fetchall()
    #pprint.pprint(records)
    
    conn.commit()

    cur.close()
    conn.close()
        

class DeputadoFederal:
    id_deputado_federal = None
    nome = None
    sexo = None
    profissao = None
    legenda = None
    uf = None
    condicao = None
    situacao = None
    matricula = None
    gabinete = None
    anexo = None
    telefone = None

    def __repr__(self):
        return "{} {} {}".format(self.nome, self.sexo, self.uf)




if __name__ == '__main__':
    main()



