import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import csv
import pandas as pd

def scrape_urls():

    driver = webdriver.Chrome("/Users/Olivia/chromedriver")

    #regular url
    #driver.get('https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NTBQS660DQ1WSwYSLmoFQNn0NNuyxKLM1JLEHLX8ohRbtfykSlu18pLoWKAkmDKCUMYQyhwqaAKhTdSKbUsqALtqISo%3D')

    #30 white wines for testing
    driver.get('https://www.vivino.com/explore?e=eJzLLbI10TNSy83MszVQy02ssDU0VUuutA0NVksGEi5qBbaGaulptmWJRZmpJYk5avlFKbZq-UmVtmrlJdGxtkZqxbYlFQDoIBYL')

    #wines = driver.find_elements(By.XPATH,"//div[@class='card__card--2R5Wh wineCard__wineCardContent--3cwZt']")
    # wines = driver.find_elements(By.XPATH, "//a[@data-testid='vintagePageLink']")
    #
    # for wine in wines:
    #     print(wine.get_attribute('href'))

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    #Code to scroll all the way down
    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    wines = driver.find_elements(By.XPATH, "//a[@data-testid='vintagePageLink']")

    urls = []
    for wine in wines:
        url = wine.get_attribute('href')
        urls.append(url)
        print(url)

    driver.close()
    return urls

'''
Scrapes individual wine page for characteristics:
-Price
-Year
-Rating
-Grape
-Region
-Tasting notes
-Food pairings
'''
def scrape_wine(url):

    driver = webdriver.Chrome("/Users/Olivia/chromedriver")
    driver.get('https://www.vivino.com/US-TX/en/villa-maria-auckland-private-bin-sauvignon-blanc/w/39034?year=2021&price_id=26743464')
    #driver.get(url)

    #Code to fully load/scroll through entire page
    driver.implicitly_wait(10)
    page_height = driver.execute_script("return document.body.scrollHeight")
    browser_window_height = driver.get_window_size(windowHandle='current')['height']
    current_position = driver.execute_script('return window.pageYOffset')
    while page_height - current_position > browser_window_height:
        driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position});")
        current_position = driver.execute_script('return window.pageYOffset')
        time.sleep(1)  # It is necessary here to give it some time to load the content

    ###################################################################################

    name = driver.find_element(By.XPATH,"//a[@class='wine']").text

    winery = driver.find_element(By.XPATH,"//a[@class='winery']").text

    price = driver.find_elements(By.XPATH, "//span[@class='purchaseAvailability__currentPrice--3mO4u']")[0].text
    price = float(price.replace('$',''))

    year = driver.find_elements(By.XPATH, "//span[@class='vintage']")[0].text
    year = int(year.split()[-1])

    rating = float(driver.find_element(By.XPATH,"//div[@class='_19ZcA']").text)

    grape = driver.find_element(By.XPATH,"//a[@data-cy='breadcrumb-grape']").text

    country = driver.find_element(By.XPATH,"//a[@data-cy='breadcrumb-country']").text

    region = driver.find_element(By.XPATH, "//a[@data-cy='breadcrumb-region']").text

    wine_type = driver.find_element(By.XPATH, "//a[@data-cy='breadcrumb-winetype']").text

    #TODO figure out how to get 4 tasting mentions
    notes = driver.find_elements(By.XPATH,"//span[@class='tasteNote__flavorGroup--1Uaen']")[0:4]
    # for element in tasting_notes:
    #     print(element.text)
    tasting_note1 = notes[0].text
    tasting_note2 = notes[1].text

    foods = driver.find_elements(By.XPATH,"//div[@class='foodPairing__foodContainer--1bvxM']/a")
    food_pairing1 = foods[0].text
    food_pairing2 = foods[1].text
    food_pairing3 = foods[2].text

    #TODO handle for red wines having tannic bar
    structure = driver.find_elements(By.XPATH,"//span[@class='indicatorBar__progress--3aXLX']")
    bold_progress = structure[0].get_attribute("style")
    boldness = float(re.findall("[+-]?\d+\.\d+", bold_progress)[0])/100

    sweet_progress = structure[1].get_attribute("style")
    sweetness = float(re.findall("[+-]?\d+\.\d+", sweet_progress)[0])/100

    acidity_progress = structure[2].get_attribute("style")
    acidity = float(re.findall("[+-]?\d+\.\d+", acidity_progress)[0])/100
    ###################################################################################

    #Put all data together into dictionary
    wine_info = dict()
    wine_info["Name"] = name
    wine_info["Winery"] = winery
    wine_info["Year"] = year
    wine_info["Price"] = price
    wine_info["Rating"] = rating
    wine_info["Type"] = wine_type
    wine_info["Grape"] = grape
    wine_info["Country"] = country
    wine_info["Region"] = region
    wine_info["Boldness"] = boldness
    wine_info["Sweetness"] = sweetness
    wine_info["Acidity"] = acidity
    wine_info["Tasting Note 1"] = tasting_note1
    wine_info["Tasting Note 2"] = tasting_note2
    wine_info["Food Pairing 1"] = food_pairing1
    wine_info["Food Pairing 2"] = food_pairing2
    wine_info["Food Pairing 3"] = food_pairing3

    return wine_info

if __name__ == "__main__":

    #urls = scrape_urls()

    #first = urls[0]
    #first = 'https://www.vivino.com/US-TX/en/villa-maria-auckland-private-bin-sauvignon-blanc/w/39034?year=2021&price_id=26743464'
    #scrape_wine(first)
    wine_info = scrape_wine("https://www.vivino.com/US-TX/en/villa-maria-auckland-private-bin-sauvignon-blanc/w/39034?year=2021&price_id=26743464")

    wines = []
    wines.append(wine_info)

    csv_columns = ["Name","Winery","Year","Price","Rating",
                   "Type","Grape","Country","Region","Boldness",
                   "Sweetness","Acidity","Tasting Note 1",
                   "Tasting Note 2","Food Pairing 1",
                   "Food Pairing 2", "Food Pairing 3"]

    file = "Wines.csv"
    try:
        with open(file,'w') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
            writer.writeheader()
            for wine in wines:
                writer.writerow(wine)
    except IOError:
        print("I/O Error")

    print("breakpoint")