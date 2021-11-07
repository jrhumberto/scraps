# https://towardsdatascience.com/selenium-in-action-2fd56ad91be6
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
import time
result_links = []
# Get all e-rate URLs from USAC data page
for i in range(2): # 2 is the total number of pages
 url = ‘https://opendata.usac.org/browse?category=E-rate&limitTo=datasets&page=' + str(i + 1)
 req = requests.get(url)
 soup = BeautifulSoup(req.content)
 erate_links = lambda tag: (getattr(tag, ‘name’, None) == ‘a’ and
 ‘href’ in tag.attrs and
 ‘e-rate’ in tag.get_text().lower())
 results = soup.find_all(erate_links)
 links = [urljoin(url, tag[‘href’]) for tag in results]
 links = [link for link in links if link.startswith(‘https://opendata.usac.org/E-rate’)]
 result_links.extend(links)
print(‘In total, there are ‘ + str(len(result_links)) + ‘ links retrieved.’)
# set up driver
driver = webdriver.Chrome()
# set up dataframe for metadata
metadata = pd.DataFrame(columns = ['Intro', 'Update Date', 'Contact', 'Email', 'Update Freq', 'URL'])
for i in range(len(result_links)):
    # extract metadata by XPATH
    data_dict = {}
    driver.get(result_links[i])
    intro = driver.find_element_by_xpath("//*[@id="app"]/div/div[2]/div[1]/section/div[2]/div/div[1]/table/tbody/tr[1]/td[2]/span").text
    update_date = driver.find_element_by_xpath("//*[@id="app"]/div/div[2]/div[1]/section/div[2]/dl/div[1]/div/div[1]/div/dd").text
    contact = driver.find_element_by_xpath("//*[@id="app"]/div/div[2]/div[1]/section/div[2]/dl/div[3]/div/div[2]/dd").text
    email = driver.find_element_by_xpath("//*[@id="app"]/div/div[2]/div[1]/section/div[2]/div/div[1]/table/tbody/tr[4]/td[2]/span/a").text
    update_freq = driver.find_element_by_xpath("//*[@id="app"]/div/div[2]/div[1]/section/div[2]/div/div[1]/table/tbody/tr[6]/td[2]/span").text
    
    # update data_dict with new metadata
    data_dict.update({'Intro': intro, 'Update Date': update_date,
                     'Contact': contact, 'Email': email, 
                     'Update Freq': update_freq, 'URL': result_links[i]})
    # update dataframe
    metadata = metadata.append(data_dict, ignore_index = True)
    
    time.sleep(5)
    action = ActionChains(driver)
    
    # Click Show More
    showmore = driver.find_element_by_xpath("//*[@id="app"]/div/div[2]/div[1]/section/div[2]/div/div[5]/a[1]")
    action.move_to_element(showmore).perform()
    showmore.click()
    time.sleep(5)
    
    # Download glossary PDFs
    glossary = driver.find_element_by_xpath("//a[contains(@href, '.pdf')]")
    glossary[0].click()
    time.sleep(5)
    
    # Click Export
    action = ActionChains(driver)
    exportmenu = driver.find_element_by_xpath("//*[@id="app"]/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/button")
    action.move_to_element(exportmenu).perform()
    exportmenu.click()
    
    # Click to download CSV file
    downloadmenu = driver.find_element_by_xpath("//*[@id="export-flannel"]/section/ul/li[1]/a")
    action.move_to_element(downloadmenu).perform()
    downloadmenu.click()
