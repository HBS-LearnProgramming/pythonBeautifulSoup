import os
import json
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def soup_generator(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def load_existing_data():
    if os.path.exists('products.json'):
        with open('products.json', 'r') as json_file:
            return json.load(json_file)
    return []

def get_last_id(existing_data):
    if existing_data:
        return max(item['ID'] for item in existing_data)
    return 0

# Setup Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver_path = 'D:/selfTry/pythonBeautifulSoup/chromedriver-win64/chromedriver.exe'

# Load existing data and start ID counter from the last used ID
existing_data = load_existing_data()
last_id = get_last_id(existing_data)
count = last_id

# Parse the HTML content to find the number of pages
pageSoup = soup_generator("https://www.newegg.ca/Gaming-Keyboards/SubCategory/ID-3523")
page_text = pageSoup.find('span', class_="list-tool-pagination-text").strong
page_num = re.findall(r'\d+', str(page_text).split("/")[1])[0]

productsDetailArr = existing_data  # Start with existing data

# Initialize the WebDriver for Selenium
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

for x in range(1, int(page_num) + 1):
    # Find all product title links
    soup = soup_generator(f"https://www.newegg.ca/Gaming-Keyboards/SubCategory/ID-3523/Page-{x}")
    products = soup.find_all('div', class_="item-cell")
    
    for product in products:
        productDetailArr = []
        
        item_info = product.find('div', class_='item-info')
        href = "Unknown href"
        itemName = "Unknown Name"
        
        if item_info.find('a', class_="item-title"):
            itemName = item_info.find('a', class_="item-title").text
            href = item_info.find('a', class_="item-title").get('href')
            
            # Selenium part to scrape detailed product options
            driver.get(href)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "form-cell"))
            )
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            product_options = soup.find_all('div', class_='form-cell')
            
            # Extract product option details
            product_options_detail = []
            for option in product_options:
                optionTypeTitle = option.find('label', class_="form-cell-name")
                if optionTypeTitle:
                    optionTypeTitle = optionTypeTitle.text.split(":")[0]
                else:
                    optionTypeTitle = "undefined"
                
                optionNames = option.find_all('li', class_="form-cell")
                optionNames = [name.text.strip() for name in optionNames] if optionNames else ["undefined"]
                
                product_options_detail.append({
                    "typeTitle": optionTypeTitle,
                    "typeName": optionNames
                })

        itemPrice = product.find('div', class_='item-action').find('ul', class_="price").find('li', class_="price-current").text
        rating_element = item_info.find('a', class_='item-rating')
        customerRate = rating_element.find("span", class_="item-rating-num").text if rating_element else "No rating"
        
        if customerRate != "No rating": 
            customerRate = re.findall(r'\d+', customerRate)[0]
        
        count += 1
        itemPrice = str(itemPrice).replace("–", " ").replace("-", " ").split("(")[0].strip()
        
        productsDetailArr.append({
            "ID": count,
            "Product_Name": itemName,
            "Price": itemPrice,
            "Rating": customerRate,
            "URL": href,
            "detail": product_options_detail
        })

# Convert the productsDetailArr to JSON format and save to file
json_data = json.dumps(productsDetailArr, indent=4)
with open('products.json', 'w') as json_file, open('backup.json', 'w') as backup_file:
    json_file.write(json_data)
    backup_file.write(json_data)

print(f"Data has been written to products.json:\n{json_data}")
