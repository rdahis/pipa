from selenium import webdriver

driver = webdriver.Firefox()
url = 'http://www.cnj.jus.br/corregedoria/justica_aberta/?'
driver.get(url)
assert driver.current_url == url
menu = driver.find_element_by_xpath("//div[@class='menu navbar']")
menu.find_elements_by_tag_name('button').click()
links = menu.find_elements_by_tag_name('a') 
import ipdb; ipdb.set_trace()
