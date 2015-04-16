#encoding: utf8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import sys, os

driver = webdriver.Firefox()
driver.implicitly_wait(0.2)
#wait = WebDriverWait(driver, 100)


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

	os.unlink('tmp/a.png')

	driver.save_screenshot('tmp/a.png')
	import ipdb;ipdb.set_trace()


def crawl_state(tag):
	driver.execute_script(tag.get_attribute('onclick'))
	municipios = driver.find_element_by_id('cidade_serventia').find_elements_by_tag_name('option')
	anos = driver.find_element_by_id('anos').find_elements_by_tag_name('option')
	#for federal, municipio, ano
	#lembrar de pular o 00
	municipio, ano = municipios[2], anos[1]
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

	driver.find_element_by_xpath("//button[text()='Pesquisar']").click()

def crawl_relatorio(relatorio):
	relatorio.click()
	table_serventia = driver.find_element_by_xpath("//strong[contains(text(), 'Produtividades da serventia')]/../..")
	relatorios = table_serventia.find_elements_by_xpath("//a/center/img/../..")
	import ipdb;ipdb.set_trace()

def execute_search():
	driver.find_element_by_xpath("//button[text()='Pesquisar']").click()

def ss():
	driver.save_screenshot('tmp/a.png')

if __name__ == '__main__':
	main()
