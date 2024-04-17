import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import xml.etree.ElementTree as ET

url = 'your-script-url-here'
response = requests.get(url)
print("response.status_code", response.status_code)
if response.status_code == 200:
    webpage_content = response.text
    # print("webpage_content", webpage_content)
else:
    print('Failed to retrieve webpage content.')
soup = BeautifulSoup(webpage_content, 'html.parser')
# print("soup", soup)
# Example: Extract book titles
# book_titles = [title.text for title in soup.find_all('div', class_='well search-list clearfix ad-container page-')]
# print("book_titles", book_titles)
  # Extract div elements with class 'well search-list'
div_elements = soup.find_all('div', class_='well search-list clearfix ad-container page-')
# print("div_elements", div_elements)
    # Extract titles from div elements
Cars_titles = [div.find('h3', class_='').text for div in div_elements]
    # Extract prices from div elements directly
prices = [div.find('div', class_='price-details generic-dark-grey').text.strip() for div in div_elements]
updates = [div.find('div', class_='pull-left dated').text for div in div_elements]
locations = [div.find('ul', class_='list-unstyled search-vehicle-info fs13').text.strip() for div in div_elements]
ratings = [div.find('span', class_='auction-rating') for div in div_elements]
vehicle_info = [{li.text.strip() for li in div.select('ul.list-unstyled.search-vehicle-info-2.fs13 li')} for div in div_elements]
# print("Cars_titles", Cars_titles, "length", len(Cars_titles))
# print("Cars_prices", prices, "length", len(prices))
# print("updates", updates, "length", len(updates))
# print("locations", locations, "length", len(locations))
# print("ratings", ratings, "length", len(ratings))
# print("vehicle_info", vehicle_info, "length", len(vehicle_info))

with sqlite3.connect("test.db") as connection:
    connection.execute("""Create table if not exists cars(
                        title varchar(255),
                        prices varchar(255),
                        locations varchar(255))
                        """)

    final_data = list(zip(Cars_titles, prices, locations))

    for i in range(len(final_data)):
        connection.execute(f"Insert into cars values (?, ?, ?)", final_data[i])

    cursor = connection.cursor()
    cursor.execute("select * from cars")
    data = cursor.fetchall()
    print(data)

    # // save as json
data = {'cars': final_data}
with open('cars.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

    # // save as xml

# Create the root element for the XML
root = ET.Element('Cars')
# Iterate through final_data to create XML elements for each vehicle
for car_data in final_data:
    car_elem = ET.SubElement(root, 'Car')
    for i, info in enumerate(car_data, 1):
        ET.SubElement(car_elem, f'Info{i}').text = info

# Create an ElementTree object and write it to an XML file
tree = ET.ElementTree(root)
tree.write('cars.xml')

