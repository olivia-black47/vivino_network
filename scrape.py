import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import csv

def scrape_urls():

    driver = webdriver.Chrome("/Users/Olivia/chromedriver")

    #url with all vivino wines
    #driver.get('https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NTBQS660DQ1WSwYSLmoFQNn0NNuyxKLM1JLEHLX8ohRbtfykSlu18pLoWKAkmDKCUMYQyhwqaAKhTdSKbUsqALtqISo%3D')

    #Red and white combo subset for testing
    driver.get('https://www.vivino.com/explore?e=eJwdi0EKgCAUBW_z1hW0_LtuEK0iwr4WQmror_T2SZuZxTAuUgtnPTVwKlMPLjSN4IoBV23HTo-K1og6EaImbRIjbIW0TRxuL-tlIhsveGVe6vCrQyLJH7DpIAY%3D')

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
    i = 0
    for wine in wines:
        url = wine.get_attribute('href')
        urls.append(url)
        print(i)
        i += 1

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
    driver.get(url)

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

    #price = driver.find_elements(By.XPATH, "//span[@class='purchaseAvailability__currentPrice--3mO4u']")[0].text
    #Some wines don't have prices
    try:
        price = driver.find_element(By.XPATH,"//div[@id='purchase-availability']").text
        price = price.split('\n')[0]
        price = float(price.replace('$',''))
    except:
        price = None

    #Some wines don't have years either I guess
    try:
        year = driver.find_elements(By.XPATH, "//span[@class='vintage']")[0].text
        year = int(year.split()[-1])
    except:
        year = None

    rating = float(driver.find_element(By.XPATH,"//div[@class='_19ZcA']").text)

    grape = driver.find_element(By.XPATH,"//a[@data-cy='breadcrumb-grape']").text

    country = driver.find_element(By.XPATH,"//a[@data-cy='breadcrumb-country']").text

    region = driver.find_element(By.XPATH, "//a[@data-cy='breadcrumb-region']").text

    wine_type = driver.find_element(By.XPATH, "//a[@data-cy='breadcrumb-winetype']").text

    notes = driver.find_elements(By.XPATH,"//span[@class='tasteNote__flavorGroup--1Uaen']")[0:4]
    tasting_note1 = notes[0].text
    tasting_note2 = notes[1].text

    #Some wines have <3 (or 0) food pairings
    try:
        foods = driver.find_elements(By.XPATH,"//div[@class='foodPairing__foodContainer--1bvxM']/a")
        food_pairing1 = foods[0].text
        food_pairing2 = foods[1].text
        food_pairing3 = foods[2].text
    except:
        food_pairing1 = ""
        food_pairing2 = ""
        food_pairing3 = ""

    #Some wines don't have structure bar
    boldness = ""
    sweetness = ""
    acidity = ""
    tannacity = ""

    try:
        structure = driver.find_elements(By.XPATH,"//span[@class='indicatorBar__progress--3aXLX']")

        #Red wines have extra structure bar
        if wine_type == "Red wine":
            bold_progress = structure[0].get_attribute("style")
            try:
                boldness = float(re.findall("\d+\.\d+", bold_progress)[0]) / 100
            except:
                boldness = float(re.findall("\d+", bold_progress)[1]) / 100

            tannic_progress = structure[1].get_attribute("style")
            try:
                tannacity = float(re.findall("\d+\.\d+", tannic_progress)[0]) / 100
            except:
                tannacity = float(re.findall("\d+", tannic_progress)[1]) / 100

            sweet_progress = structure[2].get_attribute("style")
            try:
                sweetness = float(re.findall("\d+\.\d+", sweet_progress)[0]) / 100
            except:
                sweetness = float(re.findall("\d+", sweet_progress)[1]) / 100

            acidity_progress = structure[3].get_attribute("style")
            try:
                acidity = float(re.findall("\d+\.\d+", acidity_progress)[0]) / 100
            except:
                acidity = float(re.findall("\d+", acidity_progress)[1]) / 100

        else:
            bold_progress = structure[0].get_attribute("style")
            try:
                boldness = float(re.findall("\d+\.\d+", bold_progress)[0])/100
            except:
                boldness = float(re.findall("\d+",bold_progress)[1])/100

            sweet_progress = structure[1].get_attribute("style")
            try:
                sweetness = float(re.findall("\d+\.\d+", sweet_progress)[0])/100
            except:
                sweetness = float(re.findall("\d+",sweet_progress)[1])/100

            acidity_progress = structure[2].get_attribute("style")
            try:
                acidity = float(re.findall("\d+\.\d+", acidity_progress)[0]) / 100
            except:
                acidity = float(re.findall("\d+", acidity_progress)[1]) / 100
    except:
        pass
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
    wine_info["Tannacity"] = tannacity
    wine_info["Sweetness"] = sweetness
    wine_info["Acidity"] = acidity
    wine_info["Tasting Note 1"] = tasting_note1
    wine_info["Tasting Note 2"] = tasting_note2
    wine_info["Food Pairing 1"] = food_pairing1
    wine_info["Food Pairing 2"] = food_pairing2
    wine_info["Food Pairing 3"] = food_pairing3

    driver.close()
    return wine_info

if __name__ == "__main__":

    urls = scrape_urls()
    file = "urls.csv"

    #Write url's to separate csv for funsies
    try:
        with open(file,'a',newline='') as f:
            writer = csv.writer(f)
            for url in urls:
                writer.writerow([url])
    except IOError:
        print("I/O Error")

    #Iterate through every wine url and scrape data
    wines = []
    for url in urls:
        wine_info = scrape_wine(url)
        wines.append(wine_info)

    csv_columns = ["Name","Winery","Year","Price","Rating",
                   "Type","Grape","Country","Region","Boldness",
                   "Tannacity","Sweetness","Acidity","Tasting Note 1",
                   "Tasting Note 2","Food Pairing 1",
                   "Food Pairing 2", "Food Pairing 3"]

    file = "wines.csv"
    try:
        with open(file,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
            writer.writeheader()
            for wine in wines:
                writer.writerow(wine)
    except IOError:
        print("I/O Error")