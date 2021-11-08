# https://mohitnakhale.medium.com/web-scraping-using-python-8453e6b0ead7

from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

my_tech_stack = ['python', 'git', 'django', 'angular', 'react', 'sql']

def job_finder():
    
    html_source = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_source,'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    time_stamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open(f'Job_Updates.txt','a') as f:
        f.write(f"\n ******** {time_stamp} ******** \n\n")

        for job in jobs:   
            company_name = job.find('h3', class_ = 'joblist-comp-name').text
            skills = job.find('span',class_ = 'srp-skills').text
            prettified_skills = skills.strip().replace(' ', '').split(',')
            job_link = job.header.h2.a['href']
            published_date = job.find('span', {'class': 'sim-posted' }).text
            skills_check = any(skill in my_tech_stack for skill in prettified_skills)
            
            if skills_check is True:
                f.write(f"Comapany Name: {company_name.strip()} \n")
                f.write(f"Required Skills: {skills.strip().replace(' ','')} \n")
                f.write(f"Link: {job_link} \n")
                f.write(f"Published Date: {published_date.strip()} \n")
                f.write("\n")

if __name__ == '__main__':
    while True:
        job_finder()
        time.sleep(900)
