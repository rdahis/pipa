#!/usr/bin/env python2
#encoding: utf8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import sys, os

def setup_firefox():
	driver = webdriver.Firefox()
	driver.implicitly_wait(0.2)
	handlers =  "application/pdf"
	path = "tmp/"
	driver.firefox_profile.set_preference("browser.download.folderList",1)
	driver.firefox_profile.set_preference("browser.download.manager.showWhenStarting",False)
	driver.firefox_profile.set_preference("browser.download.dir", path)
	driver.firefox_profile.set_preference("browser.download.downloadDir", path)
	driver.firefox_profile.set_preference("browser.download.defaultFolder", path)
	driver.firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
	driver.firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", handlers)
	driver.firefox_profile.set_preference("pdfjs.disabled", True)
	driver.firefox_profile.update_preferences()
	return driver

driver = setup_firefox()

def main():
	url = 'http://www.cnj.jus.br/corregedoria/justica_aberta/?'
	driver.get(url)
	assert driver.current_url == url
	menu = driver.find_element_by_xpath("//div[@class='menu navbar']")
	menu.find_element_by_tag_name('button').click()
	links = menu.find_elements_by_tag_name('a')
	menu.find_element_by_partial_link_text('1º Grau').click()
	menu.find_element_by_partial_link_text('Produtividades - Consultar por Serventia').click()

	mapinha = driver.find_element_by_tag_name('map')
	ufs = driver.find_elements_by_tag_name('area')
	ufs = [ (tag.get_attribute('title'), tag) for tag in ufs]


	#for
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
	#for serventias
	download_serventia(serventias[0])

def download_serventia(serventia): # arg: 'a' tag
	serventia.click()
	assert(len(driver.window_handles) == 2)
	driver.switch_to_window(driver.window_handles[1])
	save = driver.find_element_by_id('viewer').get_attribute('innerHTML')
	with open('tmp/name.html', 'w') as f:
		f.write(save)
	import ipdb;ipdb.set_trace()
	driver.switch_to_window(driver.window_handles[0])

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
