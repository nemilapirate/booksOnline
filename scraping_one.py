from bs4 import BeautifulSoup as bs
import requests
import csv

product_information = {"product_page_url": "https://books.toscrape.com/catalogue/a-murder-in-time_877/index.html"}

response = requests.get(product_information["product_page_url"])

if response.ok:
    soup = bs(response.text, 'html.parser')

# Récupéreration de l'universal_product_code / price_excluding_taxe / price_including_tax
informations = soup.findAll("tr")

for information in informations:
        information_label = information.find('th').text
        information_value = information.find('td').text

        target_dict = False

        if information_label == "UPC":
            target_dict = "universal_product_code"
        elif information_label == "Price (excl. tax)":
            target_dict = "price_excluding_tax"
        elif information_label == "Price (incl. tax)":
            target_dict = "price_including_tax"

        if target_dict:
            if "Â" in information_value:
                information_value = information_value.replace("Â" "£", "")

            product_information[target_dict] = information_value

# Récupéreration de image_url
product_gallery = soup.find("div", {"id": "product_gallery"})
product_information["image_url"] = "http://books.toscrape.com/" + \
product_gallery.find('img')["src"].replace('../../', '')

# Récupéreration de la categorie
breadcrumb = soup.find('ul', {"class": "breadcrumb"})
links = breadcrumb.select('li:not(.active)')
product_information["category"] = links[len(links) - 1].text.strip()

# Récupéreration du titre
product_information['title'] = soup.find('h1').text

# Récupéreration de la description et du paragraphe
description = soup.find('div', {"id": 'product_description'})
product_information["product_description"] = description.findNext('p').text

# Récupéreration de la review_rating 
review_rating = soup.find('p', {"class": "star-rating"})
if review_rating.has_attr('class'):
    review_rating = review_rating["class"][1]

    if review_rating == "One":
        review_rating = 1
    elif review_rating == "Two":
        review_rating = 2
    elif review_rating == "Three":
        review_rating = 3
    elif review_rating == "Four":
        review_rating = 4
    elif review_rating == "Five":
        review_rating = 5
    else:
        review_rating = 0
    
    product_information['review_rating'] = review_rating

    # Récupéreration du stock
    availability = soup.select('p.availability.instock')

    if availability:
        availability = availability[0].text
        availability = availability.replace('In stock (', '')
        availability = availability.replace(' available)', '')
        availability = int(availability)

        product_information["number_available"] = availability
    else:
        product_information["number_available"] = 0

# Ecriture fichier csv
with open('scraping.one.csv', 'w') as file:
    writer = csv.writer(file)

    # En têtes
    writer.writerow(product_information.keys())

    # Values
    writer.writerow(product_information.values())
