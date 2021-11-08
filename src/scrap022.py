#
# https://medium.com/@jb.ranchana/web-scraping-with-selenium-in-python-amazon-search-result-part-2-14831bb945e6
#
#
next_page = ''
driver = webdriver.Chrome(options=options, executable_path=driver_path)
...
product_asin = []
product_name = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []

items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
for item in items:
...
# store data from lists to database
store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)
global next_page
next_page = driver.find_element_by_xpath('//li[@class ="a-selected"]/following-sibling::a').get_attribute("href")
#
def scrape_amazon(keyword, max_pages):

    page_number = 1
    next_page = ''

    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.get(web)

    driver.implicitly_wait(5)
    keyword = keyword
    search = driver.find_element_by_xpath('//*[(@id = "twotabsearchtextbox")]')
    search.send_keys(keyword)
    # click search button
    search_button = driver.find_element_by_id('nav-search-submit-button')
    search_button.click()

    driver.implicitly_wait(5)

    while page_number <= max_pages:
        scrape_page(driver)
        page_number += 1
        driver.get(next_page)
        driver.implicitly_wait(5)


    driver.quit()
#
import sqlite3

def store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link):
    conn = sqlite3.connect('amazon_search.db')
    curr = conn.cursor()

    # create table
    
    curr.execute('''CREATE TABLE IF NOT EXISTS search_result (ASIN text, name text, price real, ratings text, ratings_num text, details_link text)''')
    # insert data into a table
    curr.executemany("INSERT INTO search_result (ASIN, name, price, ratings, ratings_num, details_link) VALUES (?,?,?,?,?,?)", 
                    list(zip(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)))
        
    conn.commit()
    conn.close()
