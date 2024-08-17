import json
import requests
from bs4 import BeautifulSoup

# Function to load existing data from a JSON file
def load_json_data(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)

# Function to save data to a JSON file
def save_json_data(file_name, data):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to scrape product details
def scrape_product_details(url):
    # Send a GET request to the product page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the 'product-options' divs
    product_options = soup.find_all('div', class_='form-cell')

    # Initialize a list to hold the details for the current product
    product_details = []
    optionTypeTitle = "undefined"
    optionNames = ["undefined"]

    # Loop through the product options and extract the details
    for option in product_options:
        optionTypeTitle = option.find('label', class_="form-cell-name")
        if optionTypeTitle:
            optionTypeTitle = optionTypeTitle.text.split(":")[0]

        optionNames = option.find_all('li', class_="form-cell")
        optionNames = [name.text.strip() for name in optionNames]

        product_details.append({
            "type_title": optionTypeTitle,
            "type_name": optionNames
        })

    return product_details

# Load existing products data
products_file = 'products.json'
products_data = load_json_data(products_file)

# Initialize a counter to keep track of how many products have been updated
updated_count = 0

# Loop through each product in products.json, processing the first 20 available URLs
for product in products_data:
    url = product.get("URL")
    if not product.get("product_detail"):
        # Scrape product details
        try:
            product_details = scrape_product_details(url)

            # Update the product with the extracted details
            product["product_detail"] = product_details

            # Increment the counter
            updated_count += 1

            # Break the loop after updating 20 products
            if updated_count >= 20:
                break
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue

# Save the updated products data back to products.json
save_json_data(products_file, products_data)

# Print a message to confirm the update
print(f"First {updated_count} available URLs in {products_file} have been updated with product details.")
