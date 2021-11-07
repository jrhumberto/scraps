# https://medium.com/geekculture/web-scraping-with-beautifulsoup-for-noobs-556c69b4a039
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all("article", {"class": "product_pod"})

data = []
for article in articles:

    try:
        title = article.find("img", {"class": "thumbnail"})["alt"]
        price = article.find("p", {"class": "price_color"}).text

        data.append((title, price))

    except:
        pass

df = pd.DataFrame(data, columns=["title", "price"])
df.to_csv("books.csv", index=False)
