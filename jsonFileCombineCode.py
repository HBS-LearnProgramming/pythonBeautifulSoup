import os
import json

# Function to load existing data from a JSON file
def load_json_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as json_file:
            return json.load(json_file)
    return []

# Function to get the last used ID in a dataset
def get_last_id(existing_data):
    if existing_data:
        return max(item['ID'] for item in existing_data)
    return 0

# Load data from both JSON files
products_data = load_json_data('products.json')
gaming_laptop_data = load_json_data('Gaming laptop.json')

# Get the last used ID in products.json
last_id = get_last_id(products_data)

# Start the ID counter from the last used ID in products.json
current_id = last_id

# Update the IDs in the gaming laptop data and append it to the products data
for item in gaming_laptop_data:
    current_id += 1
    item['ID'] = current_id
    products_data.append(item)

# Convert the updated products data to JSON format and save it back to products.json
json_data = json.dumps(products_data, indent=4)
with open('products.json', 'w') as json_file:
    json_file.write(json_data)

print(f"Data from 'Gaming laptop.json' has been merged into 'products.json'.")
