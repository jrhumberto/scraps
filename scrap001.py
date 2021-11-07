#import libraries
#
# https://thiagoaraujo.medium.com/python-web-scraping-with-python-to-buy-a-ps5-83fab4839fbd
#
from bs4 import BeautifulSoup #to "call" the html page (1)
import requests #to "call" the html page
import smtplib #email
import time #to set the time of updating (1)
import datetime #to set the time of updating (2)
import pandas as pd
import csv# getting the page's information
URL = 'https://www.amazon.com.br/PlayStation-Console-PlayStation%C2%AE5/dp/B088GNRX3J/ref=sr_1_1?dchild=1&keywords=playstation+5&qid=1630628596&sr=8-1&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147'


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")

soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

title = soup2.find(id='productTitle').get_text()

price = soup2.find(id='priceblock_ourprice').get_text()title1 = title.strip()
price1 = price.strip()[3:]

print(title1)
print(price1)import datetime 
today = datetime.date.today()
print(today)header =['Title','Price', 'Date']
data = [title1, price1, today]
with open('AmazonWebScraperPS5.csv', 'w', newline='', encoding ='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)df = pd.read_csv('C:/Users/thiag/AmazonWebScraperPS5.csv')
dfwith open('AmazonWebScraperPS5.csv', 'a+', newline='', encoding ='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)#appending 

def check_price8():
    URL = 'https://www.amazon.com.br/PlayStation-Console-PlayStation%C2%AE5/dp/B088GNRX3J/ref=sr_1_1?dchild=1&keywords=playstation+5&qid=1630628596&sr=8-1&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
    
    title = soup2.find(id='productTitle').get_text()
    
    price = soup2.find(id='priceblock_ourprice').get_text()
    
    title1 = title.strip()
    
    price1 = price.strip()[3:]
    
    import datetime
    
    datetime.date.today()
    
    import csv
    
    header =['Title','Price', 'Date']
    
    data = [title1, price1, today]
    
    with open('AmazonWebScraperPS5.csv', 'a+', newline='', encoding ='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    
    
    if (price1 < 6000):
        send_mail()#setting the time to update the csv file. I've choose every 6 hours. 

while(True):
    check_price8()
    time.sleep(14400)df = pd.read_csv('C:/Users/thiag/AmazonWebScraperPS5.csv')
df#sending the email everytime that the price hits less than R$ 6000

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.ehlo()
    server.login('thiagoxxxxxx@gmail.com', 'xxxxxxxxx')
    
    assunto = "O PS5 baixou de preço!"
    mensagem = "Olá, Thiago. Você criou um alerta de preço para compra do PS5 quando ele estiver menos que R$ 6000. Essa é sua chance!"
    
    msg = f"Subject: {assunto}\n\n{mensagem}"
    
    server.sendmail(
        'thiagoxxxxxx2@gmail.com',
        msg
    
    )
