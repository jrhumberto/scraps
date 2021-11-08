# https://towardsdatascience.com/top-5-beautiful-soup-functions-7bfe5a693482
#
import requests
from bs4 import BeautifulSoup
import smtplib

headers = {
    "User-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

URL = 'https://www.amazon.de/gp/product/B0756CYWWD/ref=as_li_tl?ie=UTF8&tag=idk01e-21&camp=1638&creative=6742&linkCode=as2&creativeASIN=B0756CYWWD&linkId=18730d371b945bad11e9ea58ab9d8b32'
def amazon():

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    sep = ','
    con_price = price.split(sep, 1)[0]
    converted_price = int(con_price.replace('.', ''))

    # price
    print(title.strip())
    print(converted_price)

amazon()
