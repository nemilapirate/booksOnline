
import requests
from bs4 import BeautifulSoup
import csv

def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):

    total = len(iterable)
    # Progress Bar Printing Function

    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def scrappy_products_category(soup):
    links = []

    products = soup.select('article.product_pod')

    for product in products:
        href = product.find('a')["href"]
        href = href.split('/')
        links.append("http://books.toscrape.com/catalogue/" +
                     href[-2] + "/" + href[-1])

    return links


def find_products_url_by_category(url_categ):
    # produit par page : 20
    response = requests.get(url_categ)
    links = []

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        is_pagination = soup.find("ul", {"class": "pager"})

        if is_pagination:
            nbPages = is_pagination.find(
                'li', {"class": "current"}).text.strip()
            nbPages = int(nbPages[-1:])

            if nbPages:
                for i in range(1, nbPages + 1):
                    url = url_categ.replace(
                        'index.html', 'page-' + str(i) + '.html')

                    response = requests.get(url)

                    if (response.ok):
                        soup = BeautifulSoup(response.text, 'html.parser')

                        links += scrappy_products_category(soup)
        else:
            links = scrappy_products_category(soup)

    return links

def scrappy_product(url):
    product_informations = {
        "product_page_url": url}

    response = requests.get(product_informations["product_page_url"])

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Récupérer universal_product_code / price_excluding_taxe / price_including_tax (tableau d'information en bas de page produit)
        informations = soup.findAll("tr")

        for information in informations:
            information_label = information.find('th').text
            information_value = information.find('td').text

            target_dict = False

            if (information_label == "UPC"):
                target_dict = "universal_product_code"
            elif (information_label == "Price (excl. tax)"):
                target_dict = "price_excluding_tax"
            elif (information_label == "Price (incl. tax)"):
                target_dict = "price_including_tax"

            if target_dict:
                if "Â" in information_value:
                    information_value = information_value.replace("Â", "")

                product_informations[target_dict] = information_value

        # Récupérer image_url (id product_gallery)
        product_gallery = soup.find("div", {"id": "product_gallery"})
        product_informations["image_url"] = "http://books.toscrape.com/" + \
            product_gallery.find('img')["src"]

        # Récupérer category (breadcrumbs : dernier li avant class active)
        breadcrumb = soup.find('ul', {"class": "breadcrumb"})
        links = breadcrumb.select('li:not(.active)')
        product_informations["category"] = links[len(links) - 1].text.strip()

        # Récupérer title (titre H1)
        product_informations['title'] = soup.find('h1').text

        # Récupérer description (id product_description + selecteur css frère tag p)
        description = soup.find('div', {"id": 'product_description'})

        if description:
            product_informations["product_description"] = description.findNext(
                'p').text

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

        product_informations['review_rating'] = review_rating

        # Récupérer number_available (instock outofstock en dessous du prix du produit)
        availability = soup.select('p.availability.instock')

        if availability:
            availability = availability[0].text
            availability = availability.replace('In stock (', '')
            availability = availability.replace(' available)', '')
            availability = int(availability)

            product_informations["number_available"] = availability
        else:
            product_informations["number_available"] = 0

    return product_informations


categories = []
response = requests.get('http://books.toscrape.com/')

if (response.ok):
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer toutes les catégories de livres
    for categorie in soup.select('.side_categories ul > li > ul > li > a'):
        categories.append(
            {"name": categorie.text.strip(), "url": "http://books.toscrape.com/" + categorie["href"]})

    # Consulter la page de chaque catégorie
    for categorie in progressBar(categories, prefix='Scrapping Books...:', suffix='', length=50):
        print("Catégorie : " + categorie["name"])
        links = find_products_url_by_category(categorie["url"])

        # if links:
        products_informations = []
        i = 1

        for url in links:
            products_informations.append(scrappy_product(url))

            print(str(i) + " produits scrappés sur " +
                  str(len(links)) + " produits")
            i += 1

        # Ecriture fichier csv

        with open('./csv/scraping_category.csv', 'w', encoding="utf-8") as file:
            writer = csv.DictWriter(file,fieldnames = products_informations.keys[0]())

        # En têtes et les valeurs
        writer.writeheader()
        for product_informations in products_informations:
            writer.writerow(product_informations)
