#
# https://github.com/CaioEstrella/Projeto_Scraping-Telelistas
# https://medium.com/data-hackers/web-scraping-com-python-para-preguiçosos-unindo-beautifulsoup-e-selenium-parte-2-8cfebf4f34e
#
from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
import requests
from pathlib import Path

url = "https://www.telelistas.net/rj/rio+de+janeiro"


#Informações para fingir ser um navegador
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
#juntamos tudo com a requests

html = Request(url, headers=header)
html = urlopen(html).read()
bs = BeautifulSoup(html, 'html.parser')

### Selenium

from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options  
chrome_options = Options()  
chrome_options.add_argument("--headless") 

p = str(Path(os.getcwd()))
driver = webdriver.Chrome(p +'\chromedriver.exe', options=chrome_options)
#driver.get(url)
wait = WebDriverWait(driver, 30)
#count=0
contagem = []
setores=[]
from selenium.common.exceptions import NoSuchElementException

for a in bs.find_all('a', href=True)[1:]:
    try:
        #count+=1
        
        html = Request('https://www.telelistas.net'+a['href'], headers=header)
        html = urlopen(html).read()
        
        bs = BeautifulSoup(html, 'html.parser')
        
        driver.get('https://www.telelistas.net'+a['href'])
        time.sleep(0.5)
        seto= driver.find_element_by_class_name("flex.items-center.q-breadcrumbs--last")
        con = driver.find_element_by_xpath("//div[contains(text(),'Pág')]")
        
        setores.append(seto.text)
        contagem.append(con.text)  
        print(seto.text)
        print(con.text)
        print("##")

         
    except NoSuchElementException:  #spelling error making this code not work as expected
        #count+=1
        seto = driver.find_element_by_class_name("flex.items-center.q-breadcrumbs--last")
        setores.append(seto.text)
        print(seto.text)
        print("1")
        print("##")
        contagem.append("1") 
        pass
    except:
        seto= driver.find_element_by_class_name("flex.items-center.q-breadcrumbs--last")
        setores.append(seto.text)
        print(seto.text)
        print("1")
        print("##")
        contagem.append("0") 
        pass
for count, i in enumerate(contagem):
    if len(i)>1:
        contagem[count] = i.split("/")[1]
print(len(contagem))
print(len(contagem))
print(len(setores))
setores2 = [x.split(' em Rio de Janeiro-RJ')[0] for x in setores]
contagem2 = [int(x) for x in contagem]
linhas = [25*int(x) for x in contagem]
import pandas as pd
df = pd.DataFrame({'setor': setores2, 'paginas':contagem2 , 'linhas': linhas})
df.to_excel(p+'\setores.xlsx')
