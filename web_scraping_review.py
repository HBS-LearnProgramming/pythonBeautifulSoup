from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for no GUI
chrome_options.add_argument("--disable-gpu")

# Path to your ChromeDriver
driver_path = 'D:/selfTry/pythonBeautifulSoup/chromedriver-win64/chromedriver.exe'

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# URL of the page to scrape
url = "https://www.newegg.ca/black-gigabyte-g5-series-g5-mf5-h2us354kh-gaming/p/N82E16834233584"

# Load the page with Selenium
driver.get(url)

# Wait for the comments section to load
comments_section = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "comments"))
)

# Get the page source after the comments have loaded
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Extract the 'product-options' divs
product_options = soup.find_all('div', class_='form-cell')

# Loop through the product options and find the 'form-cell' within each one
for option in product_options:
    optionTypeTitle = option.find('label', class_="form-cell-name").text.split(":")[0]
    print(optionTypeTitle)
    optionNames = option.find_all('li', class_="form-cell")
    for name in optionNames:
        print(name.text)
    

