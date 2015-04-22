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
	handlers =  "application/pdf"
	if not os.path.exists(download_path):
		os.makedirs(download_path)
	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting",False)
	profile.set_preference("browser.download.dir", download_path)
	profile.set_preference("browser.download.downloadDir", download_path)
	profile.set_preference("browser.download.defaultFolder", download_path)
	profile.set_preference("browser.helperApps.alwaysAsk.force", False)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", handlers)
	profile.set_preference("pdfjs.disabled", True)
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

	# for
	crawl_state(ufs[0][1])

	try: os.unlink('tmp/a.png')
	except OSError: pass

	driver.save_screenshot('tmp/a.png')
	import ipdb;ipdb.set_trace()


def crawl_state(tag):
	driver.execute_script(tag.get_attribute('onclick'))
	municipios = driver.find_element_by_id('cidade_serventia').find_elements_by_tag_name('option')
	anos = driver.find_element_by_id('anos').find_elements_by_tag_name('option')
	municipios, anos = municipios[1:], anos[1:] # remove the first option (useless)
	#for federal, municipio, ano
	municipio, ano = municipios[1], anos[0]
	crawl_municipio_ano(municipio, ano)

def crawl_municipio_ano(m, a):
	m.click()
	a.click()
	execute_search()
	table_prod = driver.find_element_by_id('consulta')
	# xpath do capeta q pega os 'a' que tem um filho img do tipo Produtividades
	relatorios = table_prod.find_elements_by_xpath("//a/img[@title='Produtividades']/parent::*")
	# for relatorios
	crawl_relatorio(relatorios[0])

def crawl_relatorio(relatorio):
	relatorio.click()
	table_serventia = driver.find_element_by_xpath("//strong[contains(text(), 'Produtividades da serventia')]/../..")
	serventias = table_serventia.find_elements_by_xpath("//a/center/img/../..")
	for serventia in serventias:
		download_serventia(serventia)

def download_serventia(serventia): # arg: 'a' tag
	import glob, time
	dest_file = download_path + '/' + serventia.get_attribute('onclick')
	if os.path.isfile(dest_file + '.pdf'):
		logging.info('file already downloaded')
		return False
	assert not os.path.isfile('tmp/ffdownloads/out.php') == [] , 'there is a out.php left here, aborting' + str(glob.glob('tmp/ffdownloads/out*'))
	logging.info('starting download ' + dest_file)
	serventia.click()
	assert(len(driver.window_handles) == 2)
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
	try:
		main()
	except Exception:
		ss()
		raise
