#
# https://medium.com/data-hackers/web-scraping-com-python-para-preguiçosos-unindo-beautifulsoup-e-selenium-parte-2-8cfebf4f34e
#
from bs4 import BeautifulSoup
import requests
import csv
import datetime

url = "www.web_site.com"
page = requests.get(url)

def extract(url):
    """
    Export all cryptodata from web_site.com
    website
    Arguments:
         url (str):
            url of the aimed Web_Site page
    Return:
        .csv file
    """


r = requests.session()
start = datetime.datetime.now()

for retry in range(10):
    response = r.get(url=url)
    print(response.headers)
    print("-- STATUS CODE --")
    print(response.status_code)

    if response.status_code == 200:
        with open("C:\\Users\\Username\\path\\WebScrapingCode//cryptocurrencies1_{}.csv".format(str(datetime.date.today())), "w") as f:

            fieldnames = ['name', 'price', 'coin_url', '24h_%', '7d_%', 'Market_Cap', 'Volume(24h)', 'Volume(2)', 'Circulating_Supply']
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()

soup = BeautifulSoup(page.content, 'html.parser')
cryptos = soup.find_all('table', class_="h7vnx2-2 czTsgW cmc-table")
for crypto in cryptos:
    name = cryptos.find('p', class_="sc-1eb5slv-0 iworPT").extract_first()
    price = cryptos.find('a', class_="cmc-link").extract_first()
    coin_url = cryptos.find('a', href_="cmc-link").extract_first()
    percentage_24h = cryptos.find('span', class_="sc-15yy2pl-0 hzgCfk").extract_first()
    percentage_7d = cryptos.find('span', class_="sc-15yy2pl-0 kAXKAX").extract_first()
    Market_Cap = cryptos.find('span', class_="sc-1ow4cwt-1 ieFnWP").extract_first()
    Volume_24h = cryptos.find('p', class_="sc-1eb5slv-0 hykWbK font_weight_500").extract_first()
    Volume_2 = cryptos.find('p', class_="sc-1eb5slv-0 etpvrL").extract_first()
    Circulating_Supply = cryptos.find('p', class_="sc-1eb5slv-0 kZlTnE").extract_first()

    clean_values = []
    values = [name, price, coin_url, percentage_24h, percentage_7d, Market_Cap, Volume_24h, Volume_2, Circulating_Supply]
for value in values:
    if value:
        value = value.strip().replace('\n', '')
        clean_values.append(value)

    print(', '.join(clean_values))
    dict_row = dict(zip(fieldnames, clean_values))
    writer.writerow(dict_row)

else:
    print("Page indisponible")


def main():
    url = "www.web_site.com"
    extract(url)


if __name__ == '__main__':
    main()
