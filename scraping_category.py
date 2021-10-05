import requests
from bs4 import BeautifulSoup
import csv

# Création d'une barre de progression
def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):

    total = len(iterable)
# impression de la barre de progression
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    printProgressBar(0)
    # Progression de la barre
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
#Test de progression
print("Exportation en cour...")


# Récupération des produits par catégorie
def scrappy_products_category(soup):
    links = []

    products = soup.select('article.product_pod')

    for product in products:
        href = product.find('a')["href"]
        href = href.split('/')
        links.append("http://books.toscrape.com/catalogue/" +
                     href[-2] + "/" + href[-1])

    return links

# Récupération de tous les éléments de chaque pages
def find_products_url_by_category(url_categ):
    # produit par page : 20
    response = requests.get(url_categ)
    links = []

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')

        is_pagination = soup.find("ul", {"class": "pager"})

        if is_pagination:
            nbPages = is_pagination.find(
                'li', {"class": "current"}).text.strip()
            nbPages = int(nbPages[-1:])

            if nbPages:
                for i in progressBar(range(1, nbPages + 1), prefix='Scrap Categs:', suffix='Complete', length=50):
                    url = url_categ.replace(
                        'index.html', 'page-' + str(i) + '.html')

                    response = requests.get(url)

                    if (response.ok):
                        soup = BeautifulSoup(response.text, 'html.parser')

                        links += scrappy_products_category(soup)
            else:
                print("scrapping of category url : " + url_categ)
                links = scrappy_products_category(soup)

    return links

# Récupération des information des produits
def scrappy_product(url):
    product_informations = {
        "product_page_url": url}

    response = requests.get(product_informations["product_page_url"])

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

# Récupérer l'universal_product_code / price_excluding_taxe / price_including_tax du tableau d'information produit
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

                product_informations[target_dict] = information_value

# Récupéreration image_url
        product_gallery = soup.find("div", {"id": "product_gallery"})
        product_informations["image_url"] = "http://books.toscrape.com/" + \
            product_gallery.find('img')["src"]

# Récupéreration category
        breadcrumb = soup.find('ul', {"class": "breadcrumb"})
        links = breadcrumb.select('li:not(.active)')
        product_informations["category"] = links[len(links) - 1].text.strip()

# Récupéreration des titles
        product_informations['title'] = soup.find('h1').text

# Récupéreration des descriptions et du paragraphe
        description = soup.find('div', {"id": 'product_description'})
        product_informations["product_description"] = description.findNext(
            'p').text

# Récupéreration des review_rating
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

# Récupéreration du number_available
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

category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
links = find_products_url_by_category(category_url)

if links:
    products_informations = []
    for url in progressBar(links, prefix='Scrap Products:', suffix='Complete', length=50):
        products_informations.append(scrappy_product(url))

# Ecriture fichier csv
    with open('./csv/scraping_category.csv', 'w', encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames = products_informations[0].keys())

# En têtes et les valeurs
        writer.writeheader()
        for product_informations in products_informations:
            writer.writerow(product_informations)
