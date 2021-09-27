from bs4 import BeautifulSoup as bs
import requests
import csv

product_information = {"product_page_url": "https://books.toscrape.com/catalogue/a-murder-in-time_877/index.html"}

responce = requests.get(product_information["product_page_url"])

if responce.ok:
    soup = bs(responce.text, "html.parser")

# Récupération des informations dans le tableau (UPC / Price.tax / price.Excl.tax)...
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
            information_value = information_value.replace("Â", "")

product_information[target_dict] = information_value

# Test pour voir si les éléments ont bien été séléctionner
# print(product_information)

    # Récupérer image_url (id product_gallery)
product_gallery = soup.find("div", {"id": "product_gallery"})
product_information["image_url"] = "http://books.toscrape.com/" + \
product_gallery.find('img')["src"]

    # Récupérer category (breadcrumbs : dernier li avant class active)
breadcrumb = soup.find('ul', {"class": "breadcrumb"})
links = breadcrumb.select('li:not(.active)')
product_information["category"] = links[len(links) - 1].text.strip()

    # Récupérer title (titre H1)
product_information['title'] = soup.find('h1').text

    # Récupérer description (id product_description + selecteur css frère tag p)
description = soup.find('div', {"id": 'product_description'})
product_information["product_description"] = description.findNext('p').text

    # Récupérer review_rating (class star-rating + class indiquant le nombre d'étoile)
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
else:
    review_rating = 0

product_information['review_rating'] = review_rating

# Récupérer number_available (instock outofstock en dessous du prix du produit)
availability = soup.select('p.availability.instock')

if availability:
    availability = availability[0].text
    availability = availability.replace('In stock (', '')
    availability = availability.replace(' available)', '')
    availability = int(availability)

    product_information["number_available"] = availability
else:
    product_information["number_available"] = 0

# Petit test pour vérifier que le reste des informations sont bien récupéré
# print(product_information)

with open("./csv/sraping_one.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(product_information.keys())
    writer.writerow(product_information.values())