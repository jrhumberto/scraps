# -*- coding: utf-8 -*-
# https://www.instagram.com/p/CVgZNaAsXOg/
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
browser =  webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.linkedin.com/login')

input_email= browser.find_element_by_id("username")
input_email.send_keys("hbmjunior@yahoo.com.br")

input_password= browser.find_element_by_id("password")
input_password.send_keys("iliada11")
btn_login= browser.find_element_by_xpath("//button[@type='submit']")
btn_login.click()
time.sleep(3)

busca = browser.find_element_by_xpath("//input[@placeholder='Pesquisar']")
busca.send_keys("Python")
busca.send_keys(Keys.RETURN)

time.sleep(3)

filtro_vagas = browser.find_element_by_xpath("//button[@aria-label='Vagas']")
filtro_vagas.click()
input('')
