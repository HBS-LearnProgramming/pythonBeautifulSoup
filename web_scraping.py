from bs4 import BeautifulSoup
import requests
import re
import json

def soup_generator(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

# Parse the HTML content using BeautifulSoup
pageSoup = soup_generator("https://www.newegg.ca/d/Best-Sellers/Gaming-Keyboards/s/ID-3523")
page_text = pageSoup.find('span', class_="list-tool-pagination-text").strong
page_num = re.findall(r'\d+',str(page_text).split("/")[1])[0]
productsDetailArr = []
count = 0
for x in range(int(page_num)):

    # Find all product title links
    soup = soup_generator(f"https://www.newegg.ca/d/Best-Sellers/Gaming-Keyboards/s/ID-3523/Page-{x}")
    products = soup.find_all('div', class_="item-cell")

    # Print the href attribute of each product title link
    
    
    for product in products:
        productDetailArr = []
        
        item_info = product.find('div', class_='item-info')
        itemName = item_info.find('a', class_="item-title")
        itemPrice = product.find('div', class_='item-action').find('ul', class_="price").find('li', class_="price-current").text
        
        # Attempt to find the rating element and extract the rating number if it exists
        rating_element = item_info.find('a', class_='item-rating')
        if rating_element:
            customerRate = rating_element.find("span", class_="item-rating-num")
            customerRate = customerRate.text if customerRate else ""
        else:
            customerRate = "No rating"

        itemPrice = product.find('div', class_='item-action').find('ul', class_="price").find('li', class_="price-current").text
        
        href = itemName.get('href')
        reviewPagesoup = soup_generator(href)
        if customerRate != "No rating": 
            count += 1
            customerRate = re.findall(r'\d+', customerRate)[0]
            itemPrice = str(itemPrice).replace("–", " ")
            itemPrice = str(itemPrice).replace("-", " ")
            itemPrice = itemPrice.split("(")[0]
            itemPrice = itemPrice.strip()
            productDetailArr.append(count)
            productDetailArr.append(itemName.text)
            productDetailArr.append(itemPrice)
            productDetailArr.append(customerRate)
            productDetailArr.append(href)
            CommentContent = reviewPagesoup.find_all('div', class_ = 'comments-filter-pane')
            # print(CommentContent)
        if productDetailArr:
            productsDetailArr.append({
                "ID": count,
                "Product_Name": itemName.text,
                "Price": itemPrice,
                "Rating": customerRate,
                "URL": href
            })

# Convert the productsDetailArr to JSON format
json_data = json.dumps(productsDetailArr, indent=4)

# Save the JSON data to a file
with open('products.json', 'w') as json_file:
    json_file.write(json_data)

print(f"Data has been written to products.json:\n{json_data}")
