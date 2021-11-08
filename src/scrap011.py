# https://shailchudgar005.medium.com/web-scraping-using-python-weather-data-71a8194d9c01
#
import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://forecast.weather.gov/MapClick.php?lat=41.884250000000065&lon=-87.63244999999995#.XtpdeOfhXIX"
r = requests.get(url)
soup = BeautifulSoup(r.content,"html.parser")
week = soup.find(id="seven-day-forecast-body")
items = soup.find_all("div",class_ = "tombstone-container")
period_name = [item.find(class_="period-name").get_text() for item in items]
short_desc = [item.find(class_="short-desc").get_text() for item in items]
temp = [item.find(class_="temp").get_text() for item in items]
df = pd.DataFrame({"Period" : period_name,"Short Description" : short_desc,"Temperature" : temp})
df.to_csv("18IT023_WeatherData.csv")
