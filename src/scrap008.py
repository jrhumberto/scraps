# https://medium.com/@JuanPabloHerrera/use-python-and-web-scraping-to-go-on-your-dream-vacation-ba965687e4b5
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
#######################################################################
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from password import password
#######################################################################

# This is the path where I stored my chromedriver
PATH = "/Users/juanpih19/Desktop/Programs/chromedriver"

class AirbnbBot:

    # Class constructor that takes location, stay (Month, Week, Weekend)
    # Number of guests and type of guests (Adults, Children, Infants)
    def __init__(self, location, stay, number_guests, type_guests):
        self.location = location
        self.stay = stay
        self.number_guests = number_guests
        self.type_guests = type_guests
        self.driver = webdriver.Chrome(PATH)

    # The 'search()' function will do the searching based on user input
    def search(self):

        # The driver will take us to the Airbnb website
        self.driver.get('https://www.airbnb.com')
        time.sleep(1)

        # This will find the location's tab xpath, type the desired location
        # and hit enter so we move the driver to the next tab (check in)
        location = self.driver.find_element_by_xpath('//*[@id="bigsearch-query-detached-query-input"]')
        location.send_keys(Keys.RETURN)
        location.send_keys(self.location)
        location.send_keys(Keys.RETURN)

        # It was difficult to scrape every number on the calendar
        # so both the check in and check out dates are flexible.
        flexible = location.find_element_by_xpath('//*[@id="tab--tabs--1"]')
        flexible.click()

        # Even though we have flexible dates, we can choose if
        # the stay is for the weekend or for a week or month

        # if stay is for a weekend we find the xpath, click it and hit enter
        if self.stay in ['Weekend', 'weekend']:
            weekend = self.driver.find_element_by_xpath('//*[@id="flexible_trip_lengths-weekend_trip"]/button')
            weekend.click()
            weekend.send_keys(Keys.RETURN)

        # if stay is for a  week we find the xpath, click it and hit enter
        elif self.stay in ['Week', 'week']:
            week = self.driver.find_element_by_xpath('//*[@id="flexible_trip_lengths-one_week"]/button')
            week.click()
            week.send_keys(Keys.RETURN)

        # if stay is for a month we find the xpath, click it and hit enter
        elif self.stay in ['Month', 'month']:
            month = self.driver.find_element_by_xpath('//*[@id="flexible_trip_lengths-one_month"]/button')
            month.click()
            month.send_keys(Keys.RETURN)

        else:
            pass

        # Finds the guests xpath and clicks it
        guest_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div/div[1]/div[1]/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[5]/div[1]')
        guest_button.click()

        # Based on user input self.type_guests and self.number_guests

        # if type_guests are adults
        # it will add as many adults as assigned  on self.number_guests
        if self.type_guests in ['Adults', 'adults']:
            adults = self.driver.find_element_by_xpath('//*[@id="stepper-adults"]/button[2]')
            for num in range(int(self.number_guests)):
                adults.click()

        # if type_guests are children
        # it will add as many children as assigned  on self.number_guests
        elif self.type_guests in ['Children', 'children']:
            children = self.driver.find_element_by_xpath('//*[@id="stepper-children"]/button[2]')
            for num in range(int(self.number_guests)):
                children.click()

        # if type_guests are infants
        # it will add as many infants as assigned  on self.number_guests
        elif self.type_guests in ['Infants', 'infants']:
            infants = self.driver.find_element_by_xpath('//*[@id="stepper-infants"]/button[2]')
            for num in range(int(self.number_guests)):
                infants.click()

        else:
            pass


        # Guests tab is the last tab that we need to fill before searching
        # If I hit enter the driver would not search
        # I decided to click on a random place so I could find the search's button xpath
        x = self.driver.find_element_by_xpath('//*[@id="field-guide-toggle"]')
        x.click()
        x.send_keys(Keys.RETURN)


        # I find the search button snd click in it to search for all options
        search = self.driver.find_element_by_css_selector('button._sxfp92z')
        search.click()


    # This function will scrape all the information about every option
    # on the first page
    def scraping_aribnb(self):

        # Maximize the window
        self.driver.maximize_window()

        # Gets the current page sourse
        src = self.driver.page_source

        # We create a BeautifulSoup object and feed it the current page source
        soup = BeautifulSoup(src, features='lxml')

        # Find the class that contains all the options and store it
        # on list_of_houses variable
        list_of_houses = soup.find('div', class_ = "_fhph4u")

        # Type of properties list - using find_all function
        # found the class that contains all the types of properties
        # Used a list comp to append them to list_type_property
        type_of_property = list_of_houses.find_all('div', class_="_1tanv1h")
        list_type_property = [ i.text for i in type_of_property]

        # Host description list - using find_all function
        # found the class that contains all the host descriptions
        # Used a list comp to append them to list_host_description
        host_description = list_of_houses.find_all('div', class_='_5kaapu')
        list_host_description = [ i.text for i in host_description]

        # Number of bedrooms and bathrooms - using find_all function
        # bedrooms_bathrooms and other_amenities used the same class
        # Did some slicing so I could append each item to the right list
        number_of_bedrooms_bathrooms = list_of_houses.find_all('div', class_="_3c0zz1")
        list_bedrooms_bathrooms = [ i.text for i in number_of_bedrooms_bathrooms]
        bedrooms_bathrooms = []
        other_amenities = []

        bedrooms_bathrooms = list_bedrooms_bathrooms[::2]
        other_amenities = list_bedrooms_bathrooms[1::2]

        # Date - using find_all function
        # found the class that contains all the dates
        # Used a list comp to append them to list_date
        dates = list_of_houses.find_all('div', class_="_1v92qf0")
        list_dates = [date.text for date in dates]

        # Stars - using find_all function
        # found the class that contains all the stars
        # Used a list comp to append them to list_stars
        stars = list_of_houses.find_all('div', class_ = "_1hxyyw3")
        list_stars = [star.text[:3] for star in stars]

        # Price - using find_all function
        # found the class that contains all the prices
        # Used a list comp to append them to list_prices
        prices = list_of_houses.find_all('div', class_ = "_1gi6jw3f" )
        list_prices = [price.text for price in prices ]


        # putting the lists with data into a Pandas data frame
        airbnb_data = pd.DataFrame({'Type' : list_type_property, 'Host description': list_host_description, 'Bedrooms & bathrooms': bedrooms_bathrooms, 'Other amenities': other_amenities,
                'Date': list_dates,  'Price': list_prices})

        # Saving the DataFrame to a csv file
        airbnb_data.to_csv('Airbnb_data.csv', index=False)
        
        
########################################################################################

class Traveler:

    # Email Address so user can received the filtered data
    # Stay: checks if it will be a week, month or weekend
    def __init__(self, email, stay):
        self.email = email
        self.stay = stay

    # This functtion creates a new csv file based on the options
    # that the user can afford
    def price_filter(self, amount):

        # The user will stay a month
        if self.stay in ['Month', 'month']:
            data = pd.read_csv('Airbnb_data.csv')

            # Monthly prices are usually over a $1,000.
            # Airbnb includes a comma in thousands making it hard to transform it 
            # from string to int.

            # This will create a column that takes only the digits
            # For example: $1,600 / month, this slicing will only take 1,600
            data['cleaned price'] = data['Price'].str[1:6]

            # list comp to replace every comma of every row with an empty space
            _l = [i.replace(',', '') for i in data['cleaned price']]
            data['cleaned price'] = _l

            # Once we got rid of commas, we convert every row to an int value
            int_ = [int(i) for i in data['cleaned price']]
            data['cleaned price'] = int_

            # We look for prices that are within the user's range
            # and save that to a new csv file
            result = data[data['cleaned price'] <= amount]
            return result.to_csv('filtered_data.csv', index=False)

        # The user will stay a weekend
        elif self.stay in ['Weekend', 'weekend', 'week', 'Week']:
            data = pd.read_csv('Airbnb_data.csv')

            # Prices per night are usually between 2 and 3 digits. Example: $50 or $100

            # This will create a column that takes only the digits
            # For example: $80 / night, this slicing will only take 80
            data['cleaned price'] = data['Price'].str[1:4]

            # This time I used the map() instead of list comp but it does the same thing.
            data['cleaned price'] = list(map(int, data['cleaned price']))

            # We look for prices that are within the user's range
            # and save that to a new csv file
            filtered_data = data[data['cleaned price'] <= amount]
            return filtered_data.to_csv('filtered_data.csv', index=False)

        else:
            pass

    def send_mail(self):
        # Create a multipart message
        # It takes the message body, subject, sender, receiver
        msg = MIMEMultipart()
        MESSAGE_BODY = 'Here is the list with possible options for your dream vacation'
        body_part = MIMEText(MESSAGE_BODY, 'plain')
        msg['Subject'] = "Filtered list of possible airbnb's"
        msg['From'] = 'projects.creativity.growth@gmail.com'
        msg['To'] =  self.email

        # Attaching the body part to the message
        msg.attach(body_part)

        # open and read the CSV file in binary
        with open('filtered_data.csv','rb') as file:

            # Attach the file with filename to the email
            msg.attach(MIMEApplication(file.read(), Name='filtered_data.csv'))

        # Create SMTP object
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.starttls()

        # Login to the server, email and password of the sender
        smtp_obj.login('projects.creativity.growth@gmail.com', password)

        # Convert the message to a string and send it
        smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp_obj.quit()


if __name__ == '__main__':
    vacation = AirbnbBot('New York', 'week', '2', 'adults')
    vacation.search()
    time.sleep(2)
    vacation.scraping_aribnb()
    
'''
if __name__ == "__main__":
    my_traveler = Traveler( 'juanpablacho19@gmail.com', 'week' )
    my_traveler.price_filter(80)
    my_traveler.send_mail()
'''
