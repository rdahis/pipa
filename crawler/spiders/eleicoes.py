#!/usr/bin/env python2.7

# Modules
import os

def main():
	
	# Target Directory
	dir_target = '/Users/ricardodahis/Downloads'
	
	for year in range(1998,2000,2):
		# Creates directory if necessary	
		dir = dir_target + '/eleicoes/' + str(year)
		if not os.path.exists(dir):
			os.makedirs(dir)
		# Downloads files
		for domain in ['partido', 'candidato']:
			url = url_resultados_votacao_munzona(domain, year)
			dl_unzip(url, dir)
		url = url_resultados_detalhe_votacao_munzona(year)
		dl_unzip(url, dir)
		for domain in ['consulta_cand','bem_candidato','consulta_legendas','consulta_vagas']:
			url = url_candidatos(domain, year)
			dl_unzip(url, dir)
		url = url_eleitorado(year)
		dl_unzip(url, dir)



def dl_unzip(url, dir):
	'''
	Downloads and unzips all files to directory dir.
	'''
	from zipfile import ZipFile
	from StringIO import StringIO
	local_file = dlfile(url,dir)
	with ZipFile(dir + '/' + local_file, 'r') as z:
		print('Unziping file.')
		z.extractall(dir + '/' + local_file[:-4])


def dlfile(url, dir):
	from urllib2 import URLError, HTTPError
	import requests
	# Opens the url
	try:
		local_filename = url.split('/')[-1]
		# Opens local file for download
		req = requests.get(url, stream=True)
		print('Downloading file.')
		with open(dir + '/' + local_filename, 'wb') as f:
			for chunk in req.iter_content(chunk_size=1024): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					f.flush()
					os.fsync(f.fileno())
		return local_filename
	# Handles errors
	except HTTPError, e:
		print "HTTP Error:", e.code, url
	except URLError, e:
		print "URL Error:", e.reason, url



def url_resultados_votacao_munzona(domain, year):
	'''
	domain takes values [candidato, partido]
	year takes even values between 1998 and 2010

	output: url directing to download
	'''
	url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_' + domain + '_munzona/votacao_' + domain + '_munzona_' + str(year) + '.zip'
	return url

def url_resultados_detalhe_votacao_munzona(year):
	'''
	domain takes values [secao, munzona]
	year takes even values between 1998 and 2010

	output: url directing to download
	'''
	url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_' + str(year) + '.zip'
	return url

def url_candidatos(domain, year):
	'''
	domain takes values [consulta_cand, bem_candidato, consulta_legendas, consulta_vagas]
	year takes even values between 1998 and 2010

	output: url directing to download
	'''
	url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/' + domain + '/' + domain + '_' + str(year) + '.zip'
	return url

def url_eleitorado(year):
	'''
	year takes even values between 1998 and 2010

	output: url directing to download
	'''
	url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_' + str(year) + '.zip'
	return url

if __name__ == '__main__':
	main()
