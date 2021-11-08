# https://medium.com/@muhammetbuyuknacar/automating-the-process-of-web-scraping-a-table-and-pushing-it-to-mongodb-using-python-3c40d73b9ca7
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import pymongo


def update_database():
    client = pymongo.MongoClient("mongodb+srv:/")
    db = client['']
    collection = db['']

    col_exists = '' in db.list_collection_names()

    if col_exists:
        print("collection exists")
        col = db['']
        col.drop()
        print("collection dropped")
    else:
        print("collection does not exist")

    URL = "https://www.espn.com/nba/injuries"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    header = soup.find('tr', attrs={'class': 'Table__TR Table__even'})
    columns = [col.get_text() for col in header.find_all('th')]

    final_df = pd.DataFrame(columns=columns)

    players = soup.find_all('tr', attrs={'class': re.compile('Table__TR Table__TR--sm Table__even')})

    for player in players:
        stats = [td.text for td in player.find_all('td')]
        temp_df = pd.DataFrame(stats).transpose()
        temp_df.columns = columns
        final_df = pd.concat([final_df, temp_df], ignore_index=True)

    data_dict = result_df.to_dict("records")

    action = collection.insert_many(data_dict)

    return action


def handler(event, context):
    action = update_database()
    return action
