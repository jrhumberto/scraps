# https://medium.com/@silviaonofrei/web-scraping-mini-project-4d982f29237d
#
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
options = webdriver.ChromeOptions()
options.add_argument(' — ignore-certificate-errors')
options.add_argument(' — incognito')
options.add_argument(' — headless')
url = 'https://www.udacity.com/courses/all'
driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
source = driver.get(url)
source_string = driver.page_source
soup = BeautifulSoup(source_string,'lxml')
all_courses = soup.find_all(class_ = "card_container__25DrK")
print(all_courses[0].prettify())
titles, summaries, descriptions = [], [], []
for entry in all_courses:
    titles.append(entry.find(class_="card_title__35G97").text)
    summaries.append(entry.find(class_="card_summary__1HlQ7").text)
    descriptions.append(entry.find(class_="card_flag__2XEZl").text)
courses = pd.DataFrame({'Title':titles, 'Summary':summaries, 'Type':descriptions})
courses.iloc[list(range(3))+list(range(-3,0))]
