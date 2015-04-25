#!/usr/bin/env python2
#encoding: utf8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from logging import getLogger, StreamHandler
import sys, os

download_path = "/DP/tmp/ffdownloads"
logging = getLogger(__name__)
logging.setLevel('DEBUG')
logging.addHandler(StreamHandler())
logging.info('Start application')

def setup_firefox():
	profile = webdriver.FirefoxProfile()
	del profile.DEFAULT_PREFERENCES['frozen']["browser.link.open_newwindow"] # let me live my life, the way i want to
	handlers =  "application/pdf"
	if not os.path.exists(download_path):
		os.makedirs(download_path)
	for pref, v in {
			"browser.download.folderList": 2,
			"browser.download.manager.showWhenStarting":False,
			"browser.download.dir": download_path,
			"browser.download.downloadDir": download_path,
			"browser.download.defaultFolder": download_path,
			"browser.helperApps.alwaysAsk.force": False,
			"browser.helperApps.neverAsk.saveToDisk": handlers,
			"browser.tabs.loadDivertedInBackground": True,
			"browser.link.open_newwindow": 3,
			"pdfjs.disabled": True,
			}.items():
		profile.set_preference(pref, v)
	profile.update_preferences()
	driver = webdriver.Firefox(profile)
	driver.implicitly_wait(2)
	driver.set_window_size(1200, 800)
	return driver

driver = setup_firefox()

def main():
	url = 'http://www.cnj.jus.br/corregedoria/justica_aberta/?'
	driver.get(url)
	assert driver.current_url == url
	menu = driver.find_element_by_xpath("//div[@class='menu navbar']")
	# menu.find_element_by_tag_name('button').click()
	links = menu.find_elements_by_tag_name('a')
	menu.find_element_by_partial_link_text('1º Grau').click()
	menu.find_element_by_partial_link_text('Produtividades - Consultar por Serventia').click()

	mapinha = driver.find_element_by_tag_name('map')
	ufs = driver.find_elements_by_tag_name('area')
	ufs = [ (tag.get_attribute('title'), tag) for tag in ufs]

	for uf_name, uf_tag in ufs[0:1]:
		logging.info('Crawling state:' + uf_name)
		crawl_state(uf_tag.get_attribute('onclick'))

	try: os.unlink('tmp/a.png')
	except OSError: pass

class RefreshingWebElement():
	def __init__(self, f):
		self.f = f
		self.idx = 0
		self.len = len(self.f())
	def __iter__(self): return self
	def __len__(self): return self.len
	def next(self):
		if self.idx < len(self):
			ret = self.f()[self.idx]
			self.idx += 1
			return ret
		else: raise StopIteration

def crawl_state(tag_script):
	driver.execute_script(tag_script)
	municipios = lambda: driver.find_element_by_id('cidade_serventia').find_elements_by_tag_name('option')[1:]
	anos = lambda: driver.find_element_by_id('anos').find_elements_by_tag_name('option')[1:]
	for municipio_idx in range(0, len(municipios())):
		for ano in RefreshingWebElement(anos):
			municipio = municipios()[municipio_idx]
			crawl_municipio_ano(municipio, ano)
			driver.execute_script(tag_script)

def crawl_municipio_ano(m, a):
	logging.info('crawling municipio %s on ano %s' % (m.text, a.text))
	m.click()
	a.click()
	execute_search()
	# precisa ser lambda pra re-encontrar os elementos depois do driver.back()
	table_prod = lambda: driver.find_element_by_id('consulta')

	# xpath do capeta q pega os 'a' que tem um filho img do tipo Produtividades
	relatorios = lambda: table_prod().find_elements_by_xpath("//a/img[@title='Produtividades']/..")
	for relatorio in RefreshingWebElement(relatorios):
		crawl_relatorio(relatorio)
	driver.back()

def crawl_relatorio(relatorio):
	relatorio.click()
	try:
		table_serventia = driver.find_element_by_xpath("//strong[contains(text(), 'Produtividades da serventia')]/../..")
		if u'Não existe' in table_serventia.text:
			logging.info('Empty table')
			return
		prox_pagina = table_serventia.find_element_by_id('display_next')
		while True:
			serventias = table_serventia.find_elements_by_xpath("//a/center/img/../..")
			for serventia in serventias:
				download_serventia(serventia)
			if 'disabled' in prox_pagina.get_attribute('class'):
				break
			prox_pagina.click()
	finally:
		driver.back()

def download_serventia(serventia): # arg: 'a' tag
	import glob, time
	dest_file = download_path + '/' + serventia.get_attribute('onclick')
	if os.path.isfile(dest_file + '.pdf'):
		logging.info('file already downloaded')
		return False
	assert not os.path.isfile('tmp/ffdownloads/out.php') == [] , 'there is a out.php left here, aborting' + str(glob.glob('tmp/ffdownloads/out*'))
	logging.info('starting download ' + dest_file)
	serventia.click()
	for i in range(0, 100):
		time.sleep(0.1)
		if os.path.isfile('tmp/ffdownloads/out.php') and os.path.getsize('tmp/ffdownloads/out.php'):
			break
	else: raise Exception()
	os.rename(download_path + '/out.php', dest_file + '.pdf')
	logging.info('downloaded file ' + dest_file)
	assert len(glob.glob('tmp/ffdownloads/out*.php')) == 0
	return True


def execute_search():
	driver.find_element_by_xpath("//button[text()='Pesquisar']").click()

def ss():
	driver.save_screenshot('tmp/error.png')

if __name__ == '__main__':
	from ipdb import launch_ipdb_on_exception
	with launch_ipdb_on_exception():
		try:
			main()
		except Exception as ee:
			ss()
			raise
