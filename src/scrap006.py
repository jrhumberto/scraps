# https://gohilrushabh2000.medium.com/web-scraping-using-python-6ffd059ba129
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.flipkart.com/search?q=phone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
r = requests.get(url)
content = BeautifulSoup(r.content, 'html.parser')

products = []
ratings = []
prices = []

name = content.find_all('a', {"class": "s1Q9rs"})
rate = content.find_all('div', {"class": "_3LWZlK"})
price = content.find_all('div', {"class": "_30jeq3"})

for i in name:
    products.append(i.text)
for i in range(len(products)):
    ratings.append(rate[i].text)
for i in range(len(products)):
    prices.append(price[i].text)

df = pd.DataFrame({'Product_Name': products, 'Price': prices, 'Rating': ratings})
print(df)
df.to_csv('products.csv', index=False, encoding='utf-8')
